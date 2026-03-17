import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const port = process.env.PORT || 3000;

// Resolve dhirectory name (since ES modules don't have __dirname)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.get("/c", (req, res) => {
  res.sendFile(path.join(__dirname, "c.txt"));
});

app.get("/dl", (req, res) => {
  res.sendFile(path.join(__dirname, "dl.txt"));
});

app.get("/s", (req, res) => {
  res.sendFile(path.join(__dirname, "s.txt"));
});

app.get("/ds", (req, res) => {
  res.sendFile(path.join(__dirname, "ds.txt"));
});

app.get("/eh", (req, res) => {
  res.sendFile(path.join(__dirname, "eh.txt"));
});

app.get("/v", (req, res) => {
  res.sendFile(path.join(__dirname, "v.txt"));
});

app.get("/h", (req, res) => {
  res.sendFile(path.join(__dirname, "h.txt"));
});

app.get("/a", (req, res) => {
  res.sendFile(path.join(__dirname, "a.txt"));
});

app.get("/e", (req, res) => {
  res.sendFile(path.join(__dirname, "e.txt"));
});

app.get("/d", (req, res) => {
  res.sendFile(path.join(__dirname, "d.txt"));
});

app.get("/xor", (req, res) => {
  res.sendFile(path.join(__dirname, "xor.txt"));
});

app.get("/des", (req, res) => {
  res.sendFile(path.join(__dirname, "des.txt"));
});

app.get("/k", (req, res) => {
  res.sendFile(path.join(__dirname, "k.txt"));
});

app.get("/mx", (req, res) => {
  res.sendFile(path.join(__dirname, "mx.txt"));
});

app.get("/m", (req, res) => {
  res.sendFile(path.join(__dirname, "m.txt"));
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
