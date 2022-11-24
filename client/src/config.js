// Config starter code
import { createChatBotMessage } from "react-chatbot-kit";
import CoBotAvatar from "./CoBotAvatar";

const config = {
  initialMessages: [
    createChatBotMessage(`Welcome to the Red-DSL Open Beta!`),
    createChatBotMessage(
      "Do you have a acount? If not, say [register] to create one, otherwise say [login] to login.",
      {
        delay: 400,
      }
    )
],
  customComponents: { botAvatar: (props) => <CoBotAvatar {...props} /> },
  customStyles: {
    // Overrides the chatbot message styles
    botMessageBox: {
      backgroundColor: "#376B7E",
    },
    // Overrides the chat button styles
    chatButton: {
      backgroundColor: "#5ccc9d",
    },

  }
}

export default config