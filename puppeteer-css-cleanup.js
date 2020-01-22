// Run from terminal (outputs to terminal) : node ./puppeteer-css-cleanup.js
// Save terminal to file: node ./puppeteer-css-cleanup.js > output_filename.css

const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
const page = await browser.newPage();

// URL for page being analyzed
const siteURL= 'https://wang.works/';

// Optional: Enable JS coverage (but python script can only analyze css)
await Promise.all([
    page.coverage.startJSCoverage(),
    page.coverage.startCSSCoverage()
]);

// Navigate to page
await page.goto(siteURL);

// Disable both JavaScript and CSS coverage
const [jsCoverage, cssCoverage] = await Promise.all([
    page.coverage.stopJSCoverage(),
    page.coverage.stopCSSCoverage(),
]);
let totalBytes = 0;
let usedBytes = 0;
let filenameArray =[];

// Only saving css coverage
// const coverage = [...jsCoverage, ...cssCoverage];
const coverage = [ ...cssCoverage];
for (const entry of coverage) {
    const fname = "" + entry.url;
        filenameArray.push(fname);
        // console.log(fname);
        totalBytes += entry.text.length;
        for (const range of entry.ranges){
            // console.log(range.start, range.end);
            console.log(entry.text.slice(range.start, range.end));
            usedBytes += range.end - range.start - 1;
            // final_css_bytes += entry.text.slice(range.start, range.end) + '\n';

        }

    // auto write used code to file
    //fs.writeFile('./auto_css.css', final_css_bytes, error => {
    //    if (error) {
    //        console.log('Error creating file:', error);
    //    } else {
    //        console.log('File saved');
//}
//});

}
console.log("/* =====================================================================")
console.log('=====================================================================')

console.log('Coverage for ' +  siteURL)
console.log('Files used: ');
for( const filename of filenameArray){
    console.log(""+filename);
}
console.log(`Bytes used: ${usedBytes / totalBytes * 100}%`);
console.log('===================================================================== */')


await browser.close();

})();
