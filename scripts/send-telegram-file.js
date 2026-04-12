#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { Bot, InputFile } = require('/usr/lib/node_modules/openclaw/dist/extensions/telegram/node_modules/grammy');

async function main() {
  const [,, chatId, filePath, ...captionParts] = process.argv;
  if (!chatId || !filePath) {
    console.error('Usage: send-telegram-file.js <chatId> <filePath> [caption]');
    process.exit(2);
  }
  const caption = captionParts.join(' ').trim();
  const cfg = JSON.parse(fs.readFileSync('/home/clawdy/.openclaw/openclaw.json', 'utf8'));
  const token = cfg?.channels?.telegram?.botToken;
  if (!token) throw new Error('Missing Telegram bot token in config');
  const resolved = path.resolve(filePath);
  const stat = fs.statSync(resolved);
  if (!stat.isFile()) throw new Error(`Not a file: ${resolved}`);
  const bot = new Bot(token);
  const ext = path.extname(resolved).toLowerCase();
  const input = new InputFile(resolved);
  const imageExts = new Set(['.jpg', '.jpeg', '.png', '.webp']);
  const msg = imageExts.has(ext)
    ? await bot.api.sendPhoto(chatId, input, caption ? { caption } : {})
    : await bot.api.sendDocument(chatId, input, caption ? { caption } : {});
  console.log(JSON.stringify({ ok: true, message_id: msg.message_id, chat_id: chatId, path: resolved }, null, 2));
}

main().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
