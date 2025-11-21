const fs = require("fs");
const glob = require("glob");

// Find all markdown files, but skip node_modules folder
const files = glob.sync("**/*.md", { ignore: "node_modules/**" });

// Go through each file one by one
files.forEach((file) => {
	// Read the file's content as text
	let content = fs.readFileSync(file, "utf8");

	// Find and replace markdown links with nunjucks format
	const updated = content.replace(
		/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g,
		(match, text, url) => {
			return `{% linkprimary "${text}", "${url}" %}`;
		},
	);

	// Only save the file if something changed
	if (content !== updated) {
		fs.writeFileSync(file, updated);
		console.log(`Updated: ${file}`);
	}
});

console.log("Done!");
