const fs = require("fs");
const path = require("path");

const rootDir = path.resolve(__dirname, "..");
const dataDir = path.join(rootDir, "data");
const banksPath = path.join(dataDir, "banks.json");
const outputPath = path.join(rootDir, "banks.generated.json");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function normalizeName(value) {
  return String(value || "")
    .trim()
    .replace(/\s+/g, " ");
}

const acronyms = new Set([
  "BK",
  "BNK",
  "CBC",
  "CMB",
  "COMP",
  "DEV",
  "DFCC",
  "FIN",
  "HDFC",
  "HNB",
  "LB",
  "LOLC",
  "LTD",
  "MBSL",
  "NDB",
  "PLC",
  "SL",
]);

function toTitleCase(value) {
  return normalizeName(value)
    .split(/([A-Za-z]+)/)
    .map((part) => {
      if (!/^[A-Za-z]+$/.test(part)) {
        return part;
      }

      const upper = part.toUpperCase();
      if (acronyms.has(upper)) {
        return upper;
      }

      return `${upper[0]}${upper.slice(1).toLowerCase()}`;
    })
    .join("");
}

const banks = readJson(banksPath);
const rows = [];
const emptyBranchFiles = [];
const missingBranchFiles = [];
const invalidBranchFiles = [];
const duplicateCodes = new Set();
const seenCodes = new Set();

for (const bank of banks) {
  const bankCode = String(bank.bankCode);
  const branchPath = path.join(dataDir, `${bankCode}.json`);

  if (!fs.existsSync(branchPath)) {
    missingBranchFiles.push(`${bankCode}.json`);
    continue;
  }

  const rawBranchFile = fs.readFileSync(branchPath, "utf8").trim();
  if (!rawBranchFile) {
    emptyBranchFiles.push(`${bankCode}.json`);
    continue;
  }

  let branches;
  try {
    branches = JSON.parse(rawBranchFile);
  } catch (error) {
    invalidBranchFiles.push(`${bankCode}.json: ${error.message}`);
    continue;
  }

  if (!Array.isArray(branches)) {
    invalidBranchFiles.push(`${bankCode}.json: root value is not an array`);
    continue;
  }

  for (const branch of branches) {
    if (branch.status === false) {
      continue;
    }

    const code = normalizeName(branch.branchCodeUnique);
    if (!code) {
      continue;
    }

    if (seenCodes.has(code)) {
      duplicateCodes.add(code);
    }
    seenCodes.add(code);

    rows.push({
      code,
      bankName: `${toTitleCase(bank.bankName)} / ${toTitleCase(branch.branchName)}`,
      agentOption: "SwiftCode",
      bankCountry: "SRI LANKA",
      countryCode: "LK",
    });
  }
}

rows.sort((left, right) => left.code.localeCompare(right.code));

fs.writeFileSync(outputPath, `${JSON.stringify(rows, null, 4)}\n`);

console.log(`banks: ${banks.length}`);
console.log(`generated rows: ${rows.length}`);
console.log(`empty branch files: ${emptyBranchFiles.length}`);
console.log(`missing branch files: ${missingBranchFiles.length}`);
console.log(`invalid branch files: ${invalidBranchFiles.length}`);
console.log(`duplicate codes: ${duplicateCodes.size}`);

if (emptyBranchFiles.length > 0) {
  console.log(`empty files: ${emptyBranchFiles.join(", ")}`);
}

if (missingBranchFiles.length > 0) {
  console.log(`missing files: ${missingBranchFiles.join(", ")}`);
}

if (invalidBranchFiles.length > 0) {
  console.log(`invalid files: ${invalidBranchFiles.join(", ")}`);
}

if (duplicateCodes.size > 0) {
  console.log(`duplicates: ${Array.from(duplicateCodes).join(", ")}`);
}
