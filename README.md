# watermark-pdf-python



## Requirement


 - **sudo apt-get install libmagickwand-dev** *in your terminal*
 - **pip install pdf2image**
 - **pip install wand**
 
 ## Some error handling
 Add "**\<policy domain="coder" rights="read | write" pattern="PDF" /\>**" in the */etc/ImageMagick-6/policy.xml* file before "**\</policymap\>**".
 Find the line "**\<policy domain="resource" name="disk" value="1GiB"/\>**" in the same file and replace it with  "**\<policy domain="resource" name="disk" value="8GiB"/\>**"
