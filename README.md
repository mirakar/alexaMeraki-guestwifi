# Alexa Meraki Lamba Function Package 

This repo contains many packages that are required in order to create the upload package(.ZIP) for Amazon Lambda.

There is the Meraki API (Meraki API is a wrapper around requests library to interact with the Meraki Dashboard API. It simplifies interacting with the API by keeping track of the users token, handling query and body parameters, and has the ability to execute
the request lazily.)

Finally there is the lambda_function.py which is the actual function. This file has multiple functions defined which will be called when a particular intent is called. Other packages include requests which have been downloaded in the directory.

## Scenario

<img width="830" alt="image" src="https://user-images.githubusercontent.com/22682152/132017765-66d29b40-e271-405a-ad7a-a7051f0f2d87.png">

## Prerequisites

- Cisco Meraki gear and access to the [Cisco Meraki dashboard](https://dashboard.meraki.com)
- Amazon Alexa device
- [Amazon developer account](https://developer.amazon.com)
- [AWS account](https://aws.amazon.com)

## Variables

|  Variable  |  Description  |  Where you find it in the Meraki Dashboard  |
|  ---  |  ---  |  ---  |
| **MERAKI_API_KEY** | Meraki dashboard API | [your email] > My profile > *API access** |
| **MERAKI_ORG_NAME** | name of the organization | Organizations > Settings > *Name* |
| **MERAKI_NET_NAME** | name of the network | Network-wide > General > *Network name* |
| **MERAKI_SSID_NAME** | SSID of the guest WiFi | Wireless > SSIDs > *Guest SSID name* |

*If you don’t have the token, create one with *Generate new API Key* and save it securely.

## Download lambda function and ZIP files

Save all the files in this repository.
On your local machine, navigate to the function code directory and create a ZIP package. The PPT can be omitted. 

MacOS commands:

```
// cd into the directory
cd alexaMeraki-guestwifi-master
// zip
zip -r lambda_function.zip *
```
## Next Steps

- Create the lambda function and upload the files as a ZIP
- Create an Alexa intent
- Link Alexa with the lambda function
- Test the new created Alexa skill

## Test

General instructions:
- Alexa, [intent name]
  - turn the guest wifi on 
  - turn the guest wifi on 
  - check the guest wifi password
  - check how many clients are connected to the guest wifi SSID
  - check if guest wifi is enabled/disabled
  - check why the network is slow
  - get the Meraki roadmap
  - close intent

Try it yourself:
- Alexa, ping my netowrk
  - Turn the guest WiFi on/off
  - What is the Guest WiFi password?
  - Is somebody connected
  - What is the status of the Guest WiFi?
  - Why is is everything slow?
  - Get the roadmap
  - Thank you APIs

## Additional resources

- DevNet Learning lab | [Use Alexa to configure Meraki guest network](https://developer.cisco.com/learning/lab/Meraki_Alexa/step/1)
- DevNet Meraki Develper Hub | [Dashboard with Alexa](https://developer.cisco.com/meraki/build/meraki-dashboard-with-alexa/)
- Youtube
- Presentation 

### Credits

This is from Guzmán Monné :copyright: 2017 by Guzmán Monné. License MIT, see LICENSE for more details.

