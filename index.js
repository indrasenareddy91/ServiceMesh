import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const port = process.env.PORT || 3000;

// Resolve directory name (since ES modules don't have __dirname)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.get("/servicemeshf", (req, res) => {
  res.sendFile(path.join(__dirname, "f.txt"));
});app.get("/servicemeshs", (req, res) => {
  res.sendFile(path.join(__dirname, "s.txt"));
});
// Route to serve the file
app.get("/servicemeshds", (req, res) => {
  res.sendFile(path.join(__dirname, "ds.txt"));
});
app.get("/servicemeshh", (req, res) => {
  res.sendFile(path.join(__dirname, "h.txt"));
});
app.get("/servicemesha", (req, res) => {
  res.sendFile(path.join(__dirname, "a.txt"));
});

app.get("/servicemeshdc", (req, res) => {
  res.sendFile(path.join(__dirname, "dc.txt"));
});
app.get("/servicemeshd", (req, res) => {
  res.sendFile(path.join(__dirname, "d.txt"));
});
app.get("/servicemeshx", (req, res) => {
  res.sendFile(path.join(__dirname, "xor.txt"));
});
app.get("/servicemeshk", (req, res) => {
  res.sendFile(path.join(__dirname, "k.txt"));
});
app.get("/servicemeshmx", (req, res) => {
  res.sendFile(path.join(__dirname, "mx.txt"));
});
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
