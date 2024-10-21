import React, { useEffect, useRef, useState } from 'react';
import DOMPurify from 'dompurify';
import ForumIcon from '@mui/icons-material/Forum';
import SendIcon from '@mui/icons-material/Send';
import MenuIcon from '@mui/icons-material/Menu';
import { Box, IconButton, Typography, Drawer, Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import { chatBox, chatContainer, controllerContainer, drawer, form, menu, MessageBubble, messageContainer, messageText, sendIcon } from './Styles';
import Controller from './Conroller';
import { BASE_URL } from '../../api/api';

interface FileProp {
  fileId: String,
  fileTitle: String,
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<{ role: string; content: any }[]>([]);
  const [colorMessages, setColorMessages] = useState<any>([]);
  const [sent, setSent] = useState(false);
  const [maxTokens, setMaxTokens] = useState(100);
  const [newMessage, setNewMessage] = useState('');
  const [provider, setProvider] = useState('openai');
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [systemPrompt, setSystemPrompt] = useState('You are an AI assistant.');
  const [usernameMatch, setUsernameMatch] = useState(true);
  const [file, setFile] = useState<FileProp | {}>({});
  const [searchInfo, setSearchInfo] = useState<string>("");

  // New state for controlling the reset confirmation dialog
  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const storedConversationId = localStorage.getItem('conversationId');

    if (!storedConversationId) {
      createNewConversation();
    } else {
      fetchMessages(storedConversationId);
    }
  }, []);

  const fetchMessages = async (convId: string) => {
    try {
      const response = await fetch(`${BASE_URL}/messages?conversationId=${convId}`);

      if (response.status === 404) { createNewConversation(); return; }
      if (!response.ok) throw new Error('Failed to fetch messages');

      const data = await response.json();
      setMessages(data.messages || []);
      setColorMessages(data.colorMessages || []);
      setFile(data.file || {});
      const username = localStorage.getItem('username');

      if (data.conversation.username !== username) {
        setUsernameMatch(false);
      } else {
        setUsernameMatch(true);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const createNewConversation = async () => {
    try {
      const username = localStorage.getItem('username');
      const response = await fetch(`${BASE_URL}/conversations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
      });

      if (!response.ok) throw new Error('Failed to create conversation');
      setCreateDialogOpen(false)
      const data = await response.json();
      const newConvId = data.conversationId;

      localStorage.setItem('conversationId', newConvId);
      fetchMessages(newConvId);

    } catch (error) {
      console.error('Error creating new conversation:', error);
    }
  };

  // SEND MESSAGES
  const handleSendMessage = async () => {
    if (newMessage.trim() === "") return;
    setSent(true);

    const userMessage = { role: 'user', content: newMessage };
    const updatedMessages = [...messages, userMessage];
    setNewMessage('');
    setMessages(updatedMessages);
    setColorMessages([...colorMessages, userMessage]);
    const storedConversationId = localStorage.getItem('conversationId');
    const username = localStorage.getItem('username');

    try {
      const response = await fetch(`${BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider,
          model,
          system_prompt: systemPrompt,
          messages: updatedMessages,
          conversationId: storedConversationId,
          username: username,
          fileId: (file as FileProp).fileId || null,
        }),
      });

      const data = await response.json();

      // Check if `chat_response` and its `content` and `colorContent` exist
      if (data?.chat_response) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: 'system', content: data.chat_response.content || "No content available" },
        ]);
        setColorMessages((prevColorMessages: any) => [
          ...prevColorMessages,
          { role: 'system', colorContent: data.chat_response.colorContent || "<span>No color content</span>" },
        ]);
      } else {
        console.error('Invalid response format:', data);
      }

      setSent(false);

      console.log(JSON.stringify(data.chat_response?.colorContent));
    } catch (error) {
      setSent(false);
      console.error('Error sending message:', error);
    }
  };


  // Open reset confirmation dialog
  // const handleOpenResetDialog = () => {
  //   setResetDialogOpen(true);
  // };

  // Close reset confirmation dialog
  const handleCloseResetDialog = () => {
    setResetDialogOpen(false);
  };

  // RESET MESSAGES
  const handleReset = async () => {
    const storedConversationId = localStorage.getItem('conversationId');

    if (!storedConversationId) return;

    try {
      const response = await fetch(`${BASE_URL}/reset`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ conversationId: storedConversationId }),
      });
      setResetDialogOpen(false);
      await response.json();
      setMessages([]);
      setColorMessages([]);
    } catch (error) {
      console.error('Error resetting messages:', error);
    }
  };


  // CREATE NEW CONVERSATION
  // Open create confirmation dialog
  const handleOpenCreateDialog = () => {
    setCreateDialogOpen(true);
  };

  // Close create confirmation dialog
  const handleCloseCreateDialog = () => {
    setCreateDialogOpen(false);
  };


  let debounceTimeout: ReturnType<typeof setTimeout> | null = null;

  const search = async (content: string) => {
    if (content.trim() === "") return "";
    if (!(file as FileProp)?.fileId) return "";
    try {
      const response = await fetch(`${BASE_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          fileId: (file as FileProp).fileId || null,
        }),
      });
      const data = await response.json();

      return data.question || "";
    } catch (error) {
      console.error('Error sending message:', error);
      return "";
    }
  };

  const onChangeMessage = (e: any) => {
    const inputValue = e.target.value;
    setNewMessage(inputValue);

    if (inputValue.trim() === "") return;

    if (debounceTimeout) clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(async () => {
      const question: string = await search(inputValue.trim()) || "";
      setSearchInfo(question);
    }, 500);
  };


  useEffect(() => {
    return () => {
      if (debounceTimeout) clearTimeout(debounceTimeout);
    };
  }, []);

  const pressKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      setNewMessage(searchInfo);
      setSearchInfo("");
    }
    if (e.key === "Enter") {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const afterTheValue = (text:string, value:string) => {
    let index = text.indexOf(value);
    if (index !== -1) return text.slice(index);
    return text;
  }


  return (
    <Box sx={chatContainer}>
      <Box sx={chatBox}>
        {colorMessages.length > 0 ? (
          <Box sx={messageContainer}>
            {colorMessages.map((message: any, index: number) => (
              <MessageBubble key={index} isuser={message.role === 'user' ? true : false}>
                {message.role === 'system' ? (
                  <div style={{ display: "flex" }}>
                    <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(message.colorContent) }} />
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
        ) : (
          <Box sx={{ display: 'flex', flexDirection: "column", justifyContent: "center", alignItems: "center", width: '100%', height: '100%' }}>
            <ForumIcon sx={{ fontSize: 100, color: '#DDD' }} />
            <Typography sx={{ fontFamily: 'Dosis', fontWeight: 500, color: '#888' }}>Conversation is empty. Start chatting!</Typography>
          </Box>
        )}

        {usernameMatch ? (
          <Box sx={form}>
            <div className="input-wrapper">
              <div className="placeholder" data-placeholder={(newMessage === "") ? "" : afterTheValue(searchInfo, newMessage)}>
                <input
                  title='Hello'
                  ref={inputRef}
                  value={newMessage}
                  onChange={onChangeMessage}
                  onKeyDown={pressKey}
                  className="styled-input"
                  placeholder={(newMessage === "") ? "Type your question here..." : ""}
                />
              </div>
            </div>
            <IconButton color="primary" sx={sendIcon}>
              <SendIcon onClick={handleSendMessage} sx={{ fontSize: 30 }} />
            </IconButton>
          </Box>
        ) : (
          <Typography sx={{ textAlign: 'center', fontStyle: 'italic', color: 'red' }}>
            You cannot send messages to this conversation. It belongs to another user.
          </Typography>
        )}

      </Box>

      <Box sx={controllerContainer}>
        <Controller
          file={file}
          setFile={setFile}
          model={model}
          setModel={setModel}
          provider={provider}
          maxTokens={maxTokens}
          setProvider={setProvider}
          setMaxTokens={setMaxTokens}
          systemPrompt={systemPrompt}
          setSystemPrompt={setSystemPrompt}
          // handleOpenResetDialog={handleOpenResetDialog}
          createNewConversation={handleOpenCreateDialog}
          usernameMatch={usernameMatch}
        />
      </Box>

      <Drawer anchor="right" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
        <Box sx={drawer}>
          <Controller
            file={file}
            setFile={setFile}
            model={model}
            setModel={setModel}
            provider={provider}
            maxTokens={maxTokens}
            setProvider={setProvider}
            setMaxTokens={setMaxTokens}
            systemPrompt={systemPrompt}
            setSystemPrompt={setSystemPrompt}
            // handleOpenResetDialog={handleOpenResetDialog}
            createNewConversation={handleOpenCreateDialog}
            usernameMatch={usernameMatch}
          />
        </Box>
      </Drawer>

      <IconButton sx={menu} onClick={() => setDrawerOpen(true)}>
        <MenuIcon sx={{ color: '#FFF' }} />
      </IconButton>

      {/* Reset Confirmation Dialog */}
      <Dialog open={resetDialogOpen} onClose={handleCloseResetDialog}>
        <DialogTitle>Reset Conversation</DialogTitle>
        <DialogContent>
          <Typography>Are you sure you want to reset the conversation? This action cannot be undone.</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleReset} color="primary">Yes, Reset</Button>
          <Button onClick={handleCloseResetDialog} color="secondary">Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Reset Confirmation Dialog */}
      <Dialog open={createDialogOpen} onClose={handleCloseCreateDialog}>
        <DialogTitle>Create New Conversation</DialogTitle>
        <DialogContent>
          <Typography>Are you sure you want to create new conversation!?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={createNewConversation} color="primary">Yes, Create</Button>
          <Button onClick={handleCloseCreateDialog} color="secondary">Cancel</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Chat;
