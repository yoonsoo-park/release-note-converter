import { stripHtml } from "string-strip-html";
import releaseNotes2024 from "./2024-release-notes.json" assert { type: "json" };
import fallReleaseNotes from "./releaseNotes.json" assert { type: "json" };
import fs from "fs";

let aFunction = () => {
  for (let key in fallReleaseNotes) {
    let title = fallReleaseNotes[key].Title.replace(/\s/, "_").replace(
      /\s+/g,
      "",
    );
    let body = fallReleaseNotes[key].Body__c;
    let stripedBody = stripHtml(body).result.replace(/\sx+/g, "");

    console.log("title : " + title);

    fs.writeFile(`${title}.txt`, stripedBody, (err) => {
      if (err) {
        console.error(err);
        return;
      }
      console.log("File has been created successfully.");
    });
  }
};

aFunction();
