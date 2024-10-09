import React, { useEffect, useState } from 'react';
import { Box, Typography, List, ListItem, ListItemText, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';

// const BASE_URL = "https://backend.eton.uz";
const BASE_URL = "http://127.0.0.1:5000";

type Conversation = {
    id: string;
    messages: any[];
};

type ConversationsProp = {
    username: string;
    conversations: Conversation[];
};

const Conversations: React.FC = () => {
    const [conversations, setConversations] = useState<ConversationsProp[]>([]);
    const [loading, setLoading] = useState<boolean>(true); // Add loading state
    const navigate = useNavigate();

    useEffect(() => {
        const fetchConversations = async () => {
            try {
                const username = localStorage.getItem("username");
                const response = await fetch(`${BASE_URL}/conversations?username=${username}`);
                const data = await response.json();
                setConversations(data.conversations || []);
            } catch (error) {
                console.error('Error fetching conversations:', error);
            } finally {
                setLoading(false); // Set loading to false after fetching
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
                Conversations of all users
            </Typography>

            {loading ? ( // Check if loading
                <Box display="flex" justifyContent="center" alignItems="center" height="100%">
                    <CircularProgress />
                </Box>
            ) : (
                <List>
                    {conversations.map((conversationGroup) => (
                        <Box key={conversationGroup.username} sx={{ mb: 2 }}>
                            <Typography sx={{ fontFamily: 'Dosis' }} variant="h6" gutterBottom>
                                {conversationGroup.username}
                            </Typography>
                            {conversationGroup.conversations.map((con, index) => (
                                <ListItem
                                    sx={{ cursor: 'pointer' }}
                                    key={con.id} 
                                    onClick={() => handleConversationClick(con.id)}
                                >
                                    <ListItemText
                                        primaryTypographyProps={{ sx: { fontFamily: 'Dosis' } }}
                                        primary={`Conversation ${index + 1}`} 
                                    />
                                </ListItem>
                            ))}
                        </Box>
                    ))}
                </List>
            )}
        </Box>
    );
};

export default Conversations;
