import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const port = process.env.PORT || 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const routes = {
  "/g":"g.py",
  "/e": "e.py",
  "/r": "randomized_response.py",
  "/l": "laplace-updated-credit.py",
  "/t": "t-closeness.py",
  "/x": "x-y anonymity and linkability.py",
  "/k": "k-anonymity.py",
  "/d": "l-diversity.py",
};

for (const [route, file] of Object.entries(routes)) {
  app.get(route, (req, res) => {
    res.download(path.join(__dirname, file));
  });
}

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
