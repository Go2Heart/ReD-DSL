// MessageParser starter code
import axios from 'axios';
import React from 'react';
import moment from 'moment';
const baseURL = "http://10.128.250.81:9001";



var state = "<mono_begin>";
var initializtion_progress = 0;
var token = "";
var username = "test";
var password = "test";
var timeout = 1000;
var deadline = "";
var past_user_inputs = ["hello",];
var past_bot_outputs = ["Hello, this your bank assistant. How can I help?",];
async function query(data) {
	const response = await fetch(
		"https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
		{
			headers: { Authorization: "Bearer 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" },
			method: "POST",
			body: JSON.stringify(data),
		}
	);
	const result = await response.json();
	return result;
}


const Send = (message, actions) => {
  axios.get(baseURL+"/send",{
    params: {
        state : String(state),
        msg : message,
        token : token
    },
    //responseType: 'json',
  })
  .then((response) => {
    actions.handleResponse(response.data.msg);
    state = response.data.next_state;
    timeout = response.data.timeout;
    deadline = moment().add(timeout, 'seconds').format('YYYY-MM-DD HH:mm:ss');
    if (response.data.exit === true) {
      initializtion_progress = 0;
    }
    console.log(response.data.error);
  })
  .catch((error) => {
    console.log(error.response)
    actions.handleResponse(error.response.data.msg);
  });
}

const MessageParser = ({ children, actions }) => {
  const parse = (message) => {
    if (initializtion_progress === 0) {
      state = "<mono_begin>";
      if (message === "register") {
        initializtion_progress = 1;
        actions.handleRegisterName();
      } else if (message === "login") {
        initializtion_progress = 4;
        actions.handleLoginName();
      } else {
        actions.handleResponse("Please enter [register] or [login]");
      }
    } else if(initializtion_progress === 1){
      initializtion_progress = 2;
      username = message;
      actions.handleRegisterPassword();
    } else if(initializtion_progress === 2){
      initializtion_progress = 99;
      password = message;
      axios.get(baseURL + "/register", {
        params:{
          username: username,
          password: password,
        }
      }).then((response) => {
        console.log(response.data);
        token = response.data.token;
        actions.handleResponse(response.data.msg);
        Send("<on_enter>", actions);
      }).catch((error) => {
        console.log(error);
        actions.handleResponse(error.response.data.msg + ".\nPlease input [register] to register again.\n");
        initializtion_progress = 0;
      });
    } else if(initializtion_progress === 4){
      initializtion_progress = 5;
      username = message;
      actions.handleLoginPassword();
    } else if(initializtion_progress === 5){
      initializtion_progress = 99;
      password = message;
      axios.get(baseURL + "/login", {
        params:{
          username: username,
          password: password,
        }
      }).then((response) => {
        token = response.data.token;
        actions.handleResponse(response.data.msg);
        Send("<on_enter>", actions);
      }).catch((error) => {
        console.log(error);
        actions.handleResponse(error.response.data.msg + ".\nPlease input [login] to login again.\n Or input [register] to register.\n");
        initializtion_progress = 0;
      });
    } else if(initializtion_progress === 99){
      if (moment().isAfter(deadline)) {
        Send("<on_timeout>", actions);
      }else if (message === "call") {
        initializtion_progress = 100;
        actions.handleResponse("Using AI to handle your call...\n Say anything you want to say! and I will try to understand you.\n Say [end] to exit the call.\n");
      }else {
        Send(message, actions); //normal message
      }
    } else if(initializtion_progress === 100){
      if (message === "end") {
        initializtion_progress = 99;
        actions.handleResponse("Ending call...\n");
      } else {
          query({ inputs: {
            past_user_inputs: past_user_inputs,
            generated_responses: past_bot_outputs,
            text: message,
          }})
          .then((response) => {
          console.log(response);
          actions.handleResponse(response.generated_text);
          past_user_inputs.push(message);
          past_bot_outputs.push(response.generated_text);
        });
    }
    }else {
      console.log("error");
    }
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          parse: parse,
          actions,
        });
      })}
    </div>
  );
};

export default MessageParser;