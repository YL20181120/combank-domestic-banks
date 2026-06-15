import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin
from xml.etree import ElementTree

import httpx


DOWNLOADS_URL = "https://www.lankapay.net/en/downloads"
OUTPUT_DIR = Path("downloads")
OUTPUT_FILE = OUTPUT_DIR / "lankapay-bank-branch-directory.xlsx"
GENERATED_BANKS_FILE = Path("banks.generated.json")
NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
REQUIRED_BRANCH_HEADERS = {
    "Bank Code",
    "Branch Code",
    "Branch Name",
    "Branch Address",
}
ACRONYMS = {
    "AG",
    "BK",
    "BNK",
    "CBC",
    "CDB",
    "CMB",
    "COMP",
    "DFCC",
    "FIN",
    "HDFC",
    "HNB",
    "HSBC",
    "LB",
    "LKR",
    "LOFC",
    "LOLC",
    "LTD",
    "MCB",
    "NDB",
    "NSB",
    "PLC",
    "SDB",
    "SL",
    "USD",
}


class LankaPayDownloadError(RuntimeError):
    pass


@dataclass(frozen=True)
class BranchParseResult:
    rows: list[dict[str, str]]
    skipped_rows: list[str]
    sheet_name: str


def fetch_downloads_page(client: httpx.Client) -> str:
    response = client.get(DOWNLOADS_URL)
    response.raise_for_status()
    return response.text


def find_bank_branch_directory_url(html: str) -> str:
    marker = "Bank Branch Directory"
    marker_index = html.lower().find(marker.lower())
    if marker_index == -1:
        raise LankaPayDownloadError("Could not find Bank Branch Directory on downloads page.")

    search_start = max(0, marker_index - 2000)
    search_end = min(len(html), marker_index + 4000)
    section = html[search_start:search_end]

    xlsx_index = section.lower().find(".xlsx")
    if xlsx_index == -1:
        raise LankaPayDownloadError("Could not find an xlsx download link for Bank Branch Directory.")

    href_start = section.rfind('"', 0, xlsx_index)
    href_end = section.find('"', xlsx_index)
    if href_start == -1 or href_end == -1:
        raise LankaPayDownloadError("Could not parse the Bank Branch Directory download link.")

    href = section[href_start + 1 : href_end]
    return urljoin(DOWNLOADS_URL, href)


def download_file(client: httpx.Client, url: str, output_path: Path) -> int:
    response = client.get(url)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()
    if "text/html" in content_type:
        raise LankaPayDownloadError(f"Expected Excel file but received HTML from {url}.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    return output_path.stat().st_size


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_code(value: object) -> str:
    text = normalize_text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return re.sub(r"\D", "", text)


def to_title_case(value: object) -> str:
    parts = re.split(r"([A-Za-z]+)", normalize_text(value))
    converted = []
    for part in parts:
        if not re.fullmatch(r"[A-Za-z]+", part):
            converted.append(part)
            continue

        upper = part.upper()
        if upper in ACRONYMS:
            converted.append(upper)
            continue

        converted.append(f"{upper[0]}{upper[1:].lower()}")

    return "".join(converted)


def column_name_to_index(column_name: str) -> int:
    column_index = 0
    for char in column_name:
        column_index = column_index * 26 + ord(char) - ord("A") + 1
    return column_index


def cell_column_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        raise LankaPayDownloadError(f"Could not parse cell reference: {cell_ref}")
    return column_name_to_index(match.group(1))


def read_shared_strings(workbook_zip: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in workbook_zip.namelist():
        return []

    root = ElementTree.fromstring(workbook_zip.read("xl/sharedStrings.xml"))
    strings = []
    for item in root.findall("main:si", NS):
        strings.append("".join(node.text or "" for node in item.findall(".//main:t", NS)))
    return strings


def read_sheet_paths(workbook_zip: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook_root = ElementTree.fromstring(workbook_zip.read("xl/workbook.xml"))
    rels_root = ElementTree.fromstring(workbook_zip.read("xl/_rels/workbook.xml.rels"))

    rel_targets = {}
    for rel in rels_root.findall("rel:Relationship", NS):
        target = rel.attrib["Target"]
        if not target.startswith("/"):
            target = f"xl/{target}"
        rel_targets[rel.attrib["Id"]] = target.lstrip("/")

    sheet_paths = []
    for sheet in workbook_root.findall("main:sheets/main:sheet", NS):
        rel_id = sheet.attrib[f"{{{NS['office_rel']}}}id"]
        sheet_paths.append((sheet.attrib["name"], rel_targets[rel_id]))

    return sheet_paths


def read_cell_value(cell: ElementTree.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//main:t", NS))

    value_node = cell.find("main:v", NS)
    if value_node is None or value_node.text is None:
        return ""

    value = value_node.text
    if cell_type == "s":
        return shared_strings[int(value)]

    return value


def read_sheet_rows(
    workbook_zip: zipfile.ZipFile,
    sheet_path: str,
    shared_strings: list[str],
) -> list[tuple[int, dict[int, str]]]:
    root = ElementTree.fromstring(workbook_zip.read(sheet_path))
    rows = []
    for row in root.findall(".//main:sheetData/main:row", NS):
        cells = {}
        for cell in row.findall("main:c", NS):
            value = normalize_text(read_cell_value(cell, shared_strings))
            cells[cell_column_index(cell.attrib["r"])] = value
        rows.append((int(row.attrib["r"]), cells))
    return rows


def find_branch_sheet(
    workbook_zip: zipfile.ZipFile,
    shared_strings: list[str],
) -> tuple[str, list[tuple[int, dict[int, str]]], int, dict[str, int]]:
    for sheet_name, sheet_path in read_sheet_paths(workbook_zip):
        rows = read_sheet_rows(workbook_zip, sheet_path, shared_strings)
        for row_index, cells in rows:
            headers = {value: column_index for column_index, value in cells.items()}
            if REQUIRED_BRANCH_HEADERS.issubset(headers):
                return sheet_name, rows, row_index, headers

    raise LankaPayDownloadError("Could not find branch sheet headers in the Excel file.")


def parse_branch_rows(excel_path: Path) -> BranchParseResult:
    with zipfile.ZipFile(excel_path) as workbook_zip:
        shared_strings = read_shared_strings(workbook_zip)
        sheet_name, rows, header_row_index, headers = find_branch_sheet(
            workbook_zip,
            shared_strings,
        )

    bank_code_col = headers["Bank Code"]
    branch_code_col = headers["Branch Code"]
    branch_name_col = headers["Branch Name"]

    current_bank_name = ""
    generated_rows = []
    skipped_rows = []
    seen_codes = set()

    for row_index, cells in rows:
        if row_index <= header_row_index:
            continue

        bank_code = normalize_code(cells.get(bank_code_col))
        branch_code = normalize_code(cells.get(branch_code_col))
        branch_name = normalize_text(cells.get(branch_name_col))
        non_empty_after_bank = any(
            normalize_text(cells.get(column_index))
            for column_index in range(branch_code_col, max(headers.values()) + 1)
        )

        if not bank_code and cells.get(bank_code_col) and not non_empty_after_bank:
            current_bank_name = normalize_text(cells.get(bank_code_col))
            continue

        if not any(normalize_text(value) for value in cells.values()):
            continue

        if not bank_code and not branch_code and not branch_name:
            continue

        if not bank_code or not branch_code or not branch_name:
            skipped_rows.append(
                f"row {row_index}: missing bank code, branch code, or branch name",
            )
            continue

        code = f"{bank_code}{branch_code.zfill(3)}"
        if len(code) != 7:
            skipped_rows.append(f"row {row_index}: generated code is not 7 digits ({code})")
            continue

        if code in seen_codes:
            skipped_rows.append(f"row {row_index}: duplicate code ({code})")
            continue

        seen_codes.add(code)
        bank_name = current_bank_name or bank_code
        generated_rows.append(
            {
                "code": code,
                "bankName": f"{to_title_case(bank_name)} / {to_title_case(branch_name)}",
                "agentOption": "SwiftCode",
                "bankCountry": "SRI LANKA",
                "countryCode": "LK",
            },
        )

    generated_rows.sort(key=lambda row: row["code"])
    return BranchParseResult(
        rows=generated_rows,
        skipped_rows=skipped_rows,
        sheet_name=sheet_name,
    )


def write_generated_banks(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.write_text(f"{json.dumps(rows, indent=4)}\n")


def main() -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; combank-domestic-banks/1.0)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
        html = fetch_downloads_page(client)
        download_url = find_bank_branch_directory_url(html)
        file_size = download_file(client, download_url, OUTPUT_FILE)

    if file_size == 0:
        raise LankaPayDownloadError(f"Downloaded file is empty: {OUTPUT_FILE}")

    parse_result = parse_branch_rows(OUTPUT_FILE)
    write_generated_banks(parse_result.rows, GENERATED_BANKS_FILE)

    print(f"Downloaded: {OUTPUT_FILE}")
    print(f"Source: {download_url}")
    print(f"Size: {file_size} bytes")
    print(f"Branch sheet: {parse_result.sheet_name}")
    print(f"Generated: {GENERATED_BANKS_FILE}")
    print(f"Generated rows: {len(parse_result.rows)}")
    print(f"Skipped rows: {len(parse_result.skipped_rows)}")
    for skipped_row in parse_result.skipped_rows[:10]:
        print(f"Skipped: {skipped_row}")


if __name__ == "__main__":
    main()
