# malicious_scripts_detection

data set - https://github.com/das-lab/mpsd?tab=readme-ov-file
resources - 
1. https://www.sciencedirect.com/science/article/abs/pii/S0925231221005099?via%3Dihub
2. https://posts.specterops.io/learning-machine-learning-part-1-introduction-and-revoke-obfuscation-c73033184f0
3. https://github.com/GhostPack/Invoke-Evasion/tree/main
4. https://www.microsoft.com/en-us/security/blog/2019/09/03/deep-learning-rises-new-methods-for-detecting-malicious-powershell/
5. https://arxiv.org/abs/1804.04177
6. https://www.catalyzex.com/paper/arxiv:1804.04177/code
7. https://github.com/PowerShellMafia/PowerSploit
8. https://www.cobaltstrike.com/blog/cobalt-strike-3-8-whos-your-daddy


# TO TRY:
1. Revoke-Obfuscation is a PowerShell framework that can detect obfuscated commands and scripts. To use it in your Python Jupyter notebook, you need to follow these steps:
Download the Revoke-Obfuscation module from GitHub and extract it to a folder on your system.
Import the PowerShell module in your notebook using the import_ipynb library. For example:

import import_ipynb
import RevokeObfuscation

Use the Invoke-ObfuscationDetection function to analyze a PowerShell command or script. You can pass the command or script as a string, or as a path to a file.

2.
import re

def detect_obfuscated_powershell(code):
    ### Check for common obfuscation patterns
    patterns = [
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\+\s?\w{1,10}',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\+\s?\[\w{1,10}\]',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\+\s?\$\w{1,10}',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\*\s?\w{1,10}',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\*\s?\[\w{1,10}\]',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\*\s?\$\w{1,10}',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\(\w{1,10}\)',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\(\[\w{1,10}\]\)',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\(\$\w{1,10}\)',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\(\s?\w{1,10}\s?\)',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\(\s?\[\w{1,10}\]\s?\)',
        r'\$\w{1,10}\s?=\s?\w{1,10}\s?\(\s?\$\w{1,10}\s?\)',
        r'\$[A-Za-z]{1,10}\s?=\s?ConvertTo-SecureString\s?-\w{1,10}\s?\w{1,10}\s?-\w{1,10}\s?\w{1,10}',
        r'\$[A-Za-z]{1,10}\s?=\s?ConvertFrom-SecureString\s?-\w{1,10}\s?\w{1,10}',
        r'\$[A-Za-z]{1,10}\s?=\s?@'
    ]

    ### Check if any obfuscation pattern is found
    for pattern in patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return True
    return False

### Example usage:
if _name_ == "_main_":
    sample_code = """
    $a = $b + $c
    $d = $e + [char]105
    $f = $g * $h
    $i = $j * [char]107
    $k = $l + (Get-Date)
    """
    if detect_obfuscated_powershell(sample_code):
        print("Obfuscated PowerShell code detected!")
    else:
        print("PowerShell code seems clean.")


3. https://github.com/target/Threat-Hunting/blob/master/Powershell%20Obfuscation/hunt_powershell_obfuscation.ipynb

# Note: after inspecting some benign files, there are URLs also, so it's not a good indication for malicious file, maybe it's worth to somehow check each url if it's for trusted site
To check if a URL is potentially malicious, you can use the validators Python package. Here’s how you can do it:

First, make sure you have the validators package installed. If not, you can install it using pip:
Python

!pip install validators
AI-generated code. Review and use carefully. More info on FAQ.
Now, in your Jupyter Notebook, you can use the following code snippet to validate a URL:
Python

import validators

url_to_check = "http://example.com"  # Replace with the URL you want to validate

if validators.url(url_to_check):
    print("The URL is valid.")
else:
    print("The URL is malformed or invalid.")
AI-generated code. Review and use carefully. More info on FAQ.
The validators.url() function returns True if the URL is well-formed and False otherwise. It checks for the presence of a valid scheme (e.g., “http”, “https”), a valid hostname, and other components1.
Keep in mind that this validation only ensures that the URL is properly formatted. It does not guarantee that the website is safe or non-malicious. For more advanced checks, such as detecting red flags or phishing sites, you might need additional tools or libraries.
  
# Suspicious words:
- it should not be case-sensitive
- more words: kernel32.dll, lpAddress, lpStartAddress, msvcrt.dll, ToInt32, Start-sleep, WebClient, SystemRoot, Unicode, SystemRoot, ToBase64String, VirtualAlloc

- check which words produce false-positive - and delete them

- words that are in benign scripts:
- 'key' :
  <img width="634" alt="image" src="https://github.com/TaliaSeada/malicious_scripts_detection/assets/93203695/fa6474dd-8b80-4d5b-928c-f34ffd96f39a">
- 'downloadstring' : 
  '<img width="585" alt="image" src="https://github.com/TaliaSeada/malicious_scripts_detection/assets/93203695/cbfefc40-51dd-4394-917e-fdf6b3a051f5">
- 'password' : 
<img width="581" alt="image" src="https://github.com/TaliaSeada/malicious_scripts_detection/assets/93203695/0d40e850-4fc5-46a0-8041-b33971c145ad">
- 'new object' :
<img width="343" alt="image" src="https://github.com/TaliaSeada/malicious_scripts_detection/assets/93203695/767de623-c952-4c14-b252-9fa9c1531b4f">
- 'token':
<img width="483" alt="image" src="https://github.com/TaliaSeada/malicious_scripts_detection/assets/93203695/ffd72086-6ba9-4084-a959-a8092d1b2df7">



## Summary of the article we based on:

https://www.sciencedirect.com/science/article/abs/pii/S0925231221005099?via%3Dihub

The proposed detection model of malicious PowerShell scripts based on hybrid features works by combining various levels of analysis to effectively identify malicious scripts. Here is an overview of how the model operates:

### Manual Feature Extraction:

Extracts information entropy, character distribution, and function usage from the PowerShell scripts.
Parses the script into an abstract syntax tree (AST) and calculates the distribution of 23 types of nodes from the AST, as well as the depth of the AST.
Combines these manually extracted features with features from the next part.

### Automatic Feature Extraction:

Removes comments and special characters from the scripts to reduce interference.
Converts the PowerShell script into a single line of text without punctuation, where each word is separated by a space.
Utilizes training samples to train the FastText model for word embedding.
Treats the output (label and confidence) of the FastText model as features and combines them with the manually extracted features.

### Feature Combination and Classification:

Combines the manually extracted features with the FastText model output features.
Inputs the combined features into a Random Forest classifier with specific parameters (n_estimators, max_features, random_state).
Achieves an accuracy of 97.76% in 5-fold cross-validation experiments using the detection model based on hybrid features.
By integrating manual feature extraction, automatic feature extraction, and classification using a Random Forest classifier, the model can effectively detect malicious PowerShell scripts by analyzing various aspects of the scripts at different levels .
