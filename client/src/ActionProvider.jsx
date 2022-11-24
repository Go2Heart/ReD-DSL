// in ActionProvider.jsx
import React from 'react';

function separateResponse(response) {
  var res = response.split("\n");
  return res;
}
const delay = ms => new Promise(
  resolve => setTimeout(resolve, ms)
);

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleHello = () => {
    const botMessage = createChatBotMessage('Hello. Nice\n to meet you.');
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };
  const handleResponse = async (response) => {
    var res = separateResponse(response);
    const botMessage = createChatBotMessage(res[0]);
      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage],
    }));
    for (var i = 1; i < res.length - 1; i++) {
      const botMessage = createChatBotMessage(res[i]);
      await delay(200);
      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage],
      }));
    }
  };

  const handleRegisterName = async () => {
    const botMessage = createChatBotMessage('Please enter your username');
    await delay(200);
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };
  const handleRegisterPassword = async () => {
    const botMessage = createChatBotMessage('Please enter your password');
    await delay(200);
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  const handleLoginName = async () => {
    const botMessage = createChatBotMessage('Please enter your username');
    await delay(200);
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  const handleLoginPassword = async () => {
    const botMessage = createChatBotMessage('Please enter your password');
    await delay(200);
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  // Put the handleHello function in the actions object to pass to the MessageParser
  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleHello,
            handleResponse,
            handleRegisterName,
            handleRegisterPassword,
            handleLoginName,
            handleLoginPassword,
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;