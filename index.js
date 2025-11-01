import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const port = process.env.PORT || 3000;

// Resolve directory name (since ES modules don't have __dirname)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Route to serve the file

app.get("/servicemesha", (req, res) => {
  res.sendFile(path.join(__dirname, "a.txt"));
});
app.get("/servicemeshc", (req, res) => {
  res.sendFile(path.join(__dirname, "c.txt"));
});
app.get("/servicemeshm", (req, res) => {
  res.sendFile(path.join(__dirname, "m.txt"));
});
app.get("/servicemeshmx", (req, res) => {
  res.sendFile(path.join(__dirname, "mx.txt"));
});
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
