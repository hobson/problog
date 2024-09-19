import React, { useEffect, useRef, useState } from 'react';
import DOMPurify from 'dompurify';
import Controller from './Conroller';
import { initialColorContent } from './data';
import SendIcon from '@mui/icons-material/Send';
import MenuIcon from '@mui/icons-material/Menu';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { Box, TextField, IconButton, Typography, Drawer } from '@mui/material';
import { chatBox, chatContainer, controllerContainer, drawer, form, menu, MessageBubble, messageContainer, messageText, sendIcon } from './Styles';

const Chat: React.FC = () => {

  const [messages, setMessages] = useState<{ role: string; content: any }[]>([
    // { role: 'user', content: 'Tell me about San Francisco!' },
    // { role: 'system', content: "San Francisco is a major city in California, located on the west coast of the United States. It is known for its iconic landmarks such as the Golden Gate Bridge, Alcatraz Island, and Fisherman's Wharf. The city is also famous for its hilly terrain, Victorian architecture, diverse culture, and thriving tech industry. San Francisco is home to many popular attractions, including Chinatown, the historic cable cars, and the bustling Union Square shopping district. The city is also known for its progressive values, vibrant arts scene, and delicious food offerings." }
  ]);

  const [colorMessages, setColorMessages] = useState<any>([
    // { role: 'user', content: 'Tell me about San Francisco!' },
    // {
    //   role: 'system',
    //   content: initialColorContent,
    // }
  ]);

  const [sent, setSent] = useState(false);
  const [newMessage, setNewMessage] = useState('');
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [maxTokens, setMaxTokens] = useState(100);
  const [systemPrompt, setSystemPrompt] = useState('You are an AI assistant.');
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [provider, setProvider] = useState('openai');

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // GET ALL MESSAGES
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/messages');
        const data = await response.json();
        setMessages(data.messages || []);
        setColorMessages(data.colorMessages || []);
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    };
    fetchMessages();
  }, []);

  // SEND MESSAGES!

  const handleSendMessage = async () => {
    if (newMessage.trim() === "") return;
    setSent(true)
    if (newMessage.trim()) {
      const userMessage = { role: 'user', content: newMessage };
      const updatedMessages = [...messages, userMessage];
      setNewMessage('');
      setMessages(updatedMessages);
      setColorMessages([...colorMessages, userMessage]);
      console.log("UPDATED MESSAGE =>", updatedMessages)

      try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            provider,
            model,
            system_prompt: systemPrompt,
            messages: updatedMessages
          })
        });

        const data = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: 'system', content: data.content }
        ]);

        setColorMessages((prevColorMessages: any) => [
          ...prevColorMessages,
          { role: 'system', content: data.colorContent }
        ]);
        setSent(false)
      } catch (error) {
        setSent(false)
        console.error('Error sending message:', error);
      }
    }
  };

  // RESET MESSAGES
  const handleReset = async () => {
    try {
      await fetch('http://127.0.0.1:5000/reset', {
        method: 'POST'
      });
      setMessages([]);
      setColorMessages([]);
    } catch (error) {
      console.error('Error resetting messages:', error);
    }
  };


  return (
    <Box sx={chatContainer}>
      <Box sx={chatBox}>
        <Box sx={messageContainer}>
          {colorMessages.map((message: any, index: number) => (
            <MessageBubble key={index} isuser={message.role === 'user'}>
              {message.role === 'system' ? (
                <div style={{ display: "flex" }}>
                  <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(message.content) }} />
                </div>
              ) : (
                <Typography sx={messageText} variant="body1">
                  {message.content}
                </Typography>
              )}
            </MessageBubble>
          ))}
          {sent ? (
            <Typography sx={{ fontFamily: 'Dosis' }}>
              Typing...
            </Typography>
          ) : null}
          <div ref={messagesEndRef} />
        </Box>

        <Box sx={form}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type a message..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') handleSendMessage();
            }}
          />
          <IconButton color="primary" sx={sendIcon}>
            {/* <IconButton> */}
              <RestartAltIcon onClick={handleReset} sx={{ fontSize: 30 }} />
            {/* </IconButton> */}
            <SendIcon onClick={handleSendMessage} sx={{ fontSize: 30 }} />
          </IconButton>
        </Box>
      </Box>

      <Box sx={controllerContainer}>
        <Controller
          model={model}
          setModel={setModel}
          provider={provider}
          maxTokens={maxTokens}
          setProvider={setProvider}
          setMaxTokens={setMaxTokens}
          systemPrompt={systemPrompt}
          setSystemPrompt={setSystemPrompt}
        />
      </Box>

      <Drawer anchor="right" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
        <Box sx={drawer}>
          <Controller
            model={model}
            setModel={setModel}
            provider={provider}
            maxTokens={maxTokens}
            setProvider={setProvider}
            setMaxTokens={setMaxTokens}
            systemPrompt={systemPrompt}
            setSystemPrompt={setSystemPrompt}
          />
        </Box>
      </Drawer>

      <IconButton sx={menu} onClick={() => setDrawerOpen(true)}>
        <MenuIcon />
      </IconButton>
    </Box>
  );
};

export default Chat;
