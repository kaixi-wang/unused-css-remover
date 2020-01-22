# unused-css-remover
Remove unused CSS using Puppeteer to download coverage and Python for processing

- puppeteer-css-cleanup.js: script to create a new file containing only used css from a single url

- compile_coverage_css.py: 
    - scripts for parsing styles from multiple stylesheets into a nested dict 
    - easily find conflicting definitions
    - compile and save a clean.css file containing deduplicated styles


** TODO: coverage does not yet support @keyframes, @media, @font... so deal with these separately 
