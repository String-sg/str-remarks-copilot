> [!WARNING]  
> This repo is no longer maintained. 
> For end users interested in remarks generation, please see [Remarks Co-Pilot](https://remarkscopilot.vercel.app/) instead. 

# String Remarks Co-Pilot
<img width="1025" alt="image" src="https://github.com/String-sg/str-remarks-copilot/assets/44336310/3f4a739b-9939-4ca1-b475-b323f4eed900">
<br><br>
<br>
Reduce effort with skeletal qualitative remarks by uploading structured data about students via a CSV file. This web-app provides corresponding CSV with a new output column with draft student remarks using the initial input

Disclaimer: educators are highly encouraged to review the output for accuracy 

To run on local, clone the repo
```
streamlit run app.py
```

This is a proof-of-concept app. <br>

For the full-stack re-build that is live, see https://github.com/String-sg/remarks-copilot (Ping Kahhow for access)

## Changelog <be>
_Note: this is in maintenance mode as we do the full-stack rebuild - watch this space (:_ <br>
22 Sep 2023 <br>
- Added vetters prompt for AC 

15 Aug 2023 <br>
- Added login via password or OpenAI API Key

13 Aug 2023 <br>
- Added csv template, fixed bug causing discrepancy between df and csv output 
