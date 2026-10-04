const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.env.CRM_SHARP_PATH || 'sharp');
const root = path.resolve(__dirname, '..');
const assetDir = path.join(root, 'assets');
fs.mkdirSync(assetDir, { recursive: true });

const icon = `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#4263cd"/><path d="M19 43 31 32 46 20" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="19" cy="43" r="6" fill="#fff"/><circle cx="31" cy="32" r="6" fill="#9cdbff"/><circle cx="46" cy="20" r="6" fill="#fff"/></svg>`;
fs.writeFileSync(path.join(assetDir, 'favicon.svg'), icon);

async function main() {
  for (const [name, size] of [['favicon-32.png', 32], ['apple-touch-icon.png', 180], ['icon-192.png', 192], ['icon-512.png', 512]]) {
    await sharp(Buffer.from(icon)).resize(size, size).png().toFile(path.join(assetDir, name));
  }
  const png = fs.readFileSync(path.join(assetDir, 'favicon-32.png'));
  const header = Buffer.alloc(22);
  header.writeUInt16LE(1, 2); header.writeUInt16LE(1, 4);
  header[6] = 32; header[7] = 32;
  header.writeUInt16LE(1, 10); header.writeUInt16LE(32, 12);
  header.writeUInt32LE(png.length, 14); header.writeUInt32LE(22, 18);
  fs.writeFileSync(path.join(root, 'favicon.ico'), Buffer.concat([header, png]));
  // Sharing image: run scripts/build-og.py after generating the latest screenshots.
  console.log('Created favicon and app icons.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
