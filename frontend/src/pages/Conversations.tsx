import React, { useEffect, useState } from 'react';
import { Box, Typography, List, ListItem, ListItemText } from '@mui/material';
import { useNavigate } from 'react-router-dom';

type Conversation = {
    _id: string;
};

const Conversations: React.FC = () => {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchConversations = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/conversations');
                const data = await response.json();
                setConversations(data.conversations || []);
            } catch (error) {
                console.error('Error fetching conversations:', error);
            }
        };

        fetchConversations();
    }, []);


    const handleConversationClick = (conversationId: string) => {
        localStorage.setItem('conversationId', conversationId);
        navigate('/');
    };

    return (
        <Box sx={{ padding: 2 }}>
            <Typography sx={{ fontFamily: 'Dosis' }} variant="h4" gutterBottom>
                Conversations ({conversations.length})
            </Typography>

            <List>
                {conversations.map((conversation, index) => (
                    <ListItem
                        sx={{ cursor: 'pointer' }}
                        key={conversation._id}
                        divider
                        onClick={() => handleConversationClick(conversation._id)}
                    >
                        <ListItemText
                            primaryTypographyProps={{ sx: { fontFamily: 'Dosis' } }}
                            primary={`conversation-${index + 1}`}
                        />
                    </ListItem>
                ))}
            </List>
        </Box>
    );
};

export default Conversations;
