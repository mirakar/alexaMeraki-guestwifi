'''
 * This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK (v2).
 * Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
 * session persistence, api calls, and more.
'''

from __future__ import print_function
from meraki_api import MerakiAPI
import requests
import json
import re
import os

def get_org_by_name(meraki, name):
    orgs = meraki.organizations().index().json()
    for item in orgs:
        if item['name'] == name:
            return item
    raise ValueError("not found: name={}".format(name))

def get_network_by_name(meraki, org_id, name):
    nets = meraki.organizations(org_id).networks().index().json()
    for item in nets:
        if item['name'] == name:
            return item
    raise ValueError("not found: org_id={} name={}".format(org_id, name))

def get_ssid_by_name(meraki, org_id, net_id, name):
    ssids = meraki.organizations(org_id).networks(net_id).ssids().index().json()
    for item in ssids:
        if item['name'] == name:
            return item
    raise ValueError("not found: org_id={} net_id={} name={}".format(org_id, net_id, name))

# def meraki.organizations(ORGID).networks().index().json()

####################################################

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_orgs_response():
    session_attributes = {}
    card_title = "My Meraki Organizations"
    response = meraki.organizations().index()
    json = response.json()
    print(json)
    speech_output = "{0} - organizations found, {1}".format(str(len(json)), json[0]['name'])
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hi from the Meraki Dashboard. How can I help you?" 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Meraki Dashboard is still waiting for your orders." 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_network_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "networks"
    speech_output = "Nothing implemented yet " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Nothing implemented yet " 
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "The power of Meraki Cloud at your service! " \
                    "See you later aligator!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(guest_network, intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent_name)
    # Dispatch to your skill's intent handlers
    if intent_name == "guestnetON":
        return guest_network.enable()
    if intent_name == "guestnetOFF":
        return guest_network.disable()
    if intent_name == "guestnetPASSWORD":
        return guest_network.password()
    if intent_name == "guestnetSTATUS":
        return guest_network.checkstatus()
    if intent_name == "guestnetDEVICES":
        return guest_network.numdevices()
    if intent_name == "guestnetTRAFFIC":
        return guest_network.why_internet_slow()
    if intent_name == "roadmap":
        return guest_network.get_roadmap()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

class GuestNetwork:
    def __init__(self, meraki, meraki_apikey, org_id, net_id, ssid):
        self.meraki             = meraki
        self.meraki_apikey      = meraki_apikey
        self.org_id             = org_id
        self.net_id             = net_id
        self.ssid               = ssid

    def getdevices(self):
        
        url = "https://api.meraki.com/api/v0/networks/" + self.net_id + "/clients"
        headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-Cisco-Meraki-API-Key": self.meraki_apikey
                    }
        response = requests.request('GET', url, headers=headers)
        return response.json() 
        
        #enable the guest Wi-FI
    def enable(self):
        session_attributes = {}
        card_title = "Guest Network On"
        reprompt_text = ""
        response = self.meraki.organizations(self.org_id).networks(self.net_id).ssids(self.ssid['number']).update({"enabled": True})
        if response.status_code == 200:
            speech_output = "Success ! Enabling guest wi-fi"
        else:
            speech_output = "Sorry could not Enable Guest Wi-fi"
        print(speech_output)
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))

        #disable the guest Wi-Fi
    def disable(self):
        session_attributes = {}
        card_title = "Guest Network Off"
        reprompt_text = ""
        response = self.meraki.organizations(self.org_id).networks(self.net_id).ssids(self.ssid['number']).update({"enabled": False})
        if response.status_code == 200:
            speech_output = "Success ! Disabled guest wi-fi"
        else:
            speech_output = "Sorry could not Disable Guest Wi-fi"
        print(speech_output)
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))

        #share the Guest Wi-Fi password
    def password(self):
        session_attributes = {}
        card_title = "Guest Network Password"
        reprompt_text = ""
        response =self.meraki.organizations(self.org_id).networks(self.net_id).ssids(self.ssid['number']).index().json()['authMode']
        if response == "open":
            speech_output = "There is no password for this Guest Wi-Fi. Just connect, click through the splash page and enjoy!"
        else:
            speech_output = "The password for {0} - is {1}".format(str(self.ssid['name']),  self.ssid['psk'])
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

        #check if the Guest Wi-Fi is enabled or disabled
    def checkstatus(self):
        session_attributes = {}
        card_title = "Check Status"
        reprompt_text = ""
        #devces = getdevices(self)
        response = self.meraki.organizations(self.org_id).networks(self.net_id).ssids(self.ssid['number']).index().json()['enabled']
        if response:
            speech_output = "Guest Wi-Fi is enabled!"
        else:
            speech_output = "Guest Wi-Fi is disabled!"
        print(speech_output)
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))
     
        #check the number of devices that are connected on the guest Wi-Fi
    def numdevices(self):
        session_attributes = {}
        reprompt_text = None
        card_title = "Number of devices"
        
        num_device = len([device for device in self.getdevices() if device['ssid'] == self.ssid])
        
        speech_output = 'The number of connected devices is {0}'.format(num_device)
        print(speech_output)
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))
    
        
    
    def getnetworktrafficstats(self):
        #https://developer.cisco.com/meraki/api/#!get-network-traffic
        url = "https://api.meraki.com/api/v0/networks/" + self.net_id + "/traffic?timespan=86400&deviceType=combined"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": self.meraki_apikey
                    }
        response = requests.request('GET', url, headers=headers)
        return response.json()        

        #check the network traffic
    def why_internet_slow(self):
         
        session_attributes = {}
        reprompt_text = None
        card_title = "Why is the conncetion slow?"
        
        #86400 seconds = 24 hours 
        TIMESTAMP = 86400
        
        clients = self.getdevices()
        usage = [client['usage']['sent'] + client['usage']['recv'] for client in clients]
        max_client = clients[usage.index(max(usage))]
        bw_use = round((max_client['usage']['sent'] + max_client['usage']['recv']) / 1024)
    
        traffic = self.getnetworktrafficstats()
        applications = [app['application'] for app in traffic]
        bws = [app['recv'] + app['sent'] for app in traffic]
        max_bw = max(bws)
        max_app = applications[bws.index(max_bw)]
    
        speech_output = 'That\'s because among the {0} clients connected, the top bandwidth hog is {1}. That device used {2} megabytes of data in the last {3}, {4} percent just on {5}.'.format(len(clients), max_client['description'], bw_use, ('hour' if TIMESTAMP == 3600 else str(round(TIMESTAMP / 60 / 60)) + ' hours'), round((max_bw / 1024) / bw_use * 100), max_app)
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))

        # an easter egg for Merakians =)
    def get_roadmap(self):
        session_attributes = {}
        card_title = "Roadmap"
        reprompt_text = None
        speech_output = 'The first rule of Meraki roadmaps, ' \
                        'is we do not talk about Meraki roadmaps.'
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))
        
# --------------- Main handler ------------------

def lambda_handler(event, context):
    MERAKI_API_KEY   = os.environ['MERAKI_API_KEY']
    MERAKI_ORG_NAME  = os.environ['MERAKI_ORG_NAME']
    MERAKI_NET_NAME  = os.environ['MERAKI_NET_NAME']
    MERAKI_SSID_NAME = os.environ['MERAKI_SSID_NAME']

    meraki           = MerakiAPI(MERAKI_API_KEY)
    org              = get_org_by_name(meraki, MERAKI_ORG_NAME)
    net              = get_network_by_name(meraki, org['id'], MERAKI_NET_NAME)
    ssid             = get_ssid_by_name(meraki, org['id'], net['id'], MERAKI_SSID_NAME)
    guest_network    = GuestNetwork(meraki, MERAKI_API_KEY, org['id'], net['id'], ssid)
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    # """
    # Uncomment this if statement and populate with your skill's application ID to
    # prevent someone else from configuring a skill that sends requests to this
    # function.
    # """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(guest_network, event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
