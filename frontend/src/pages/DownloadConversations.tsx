import React, { useEffect, useState } from 'react';
import { Box, Typography, List, ListItem, ListItemText, IconButton, CircularProgress, Snackbar, Alert } from '@mui/material';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import { BASE_URL } from '../api/api';

type Conversation = {
    id: string;
    messages: any[];
};

type ConversationsProp = {
    username: string;
    conversations: Conversation[];
};

const DownloadConversations: React.FC = () => {
    const [conversations, setConversations] = useState<ConversationsProp[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [downloading, setDownloading] = useState<string | null>(null); 
    const [showSuccessAlert, setShowSuccessAlert] = useState<boolean>(false); 

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
                setLoading(false);
            }
        };

        fetchConversations();
    }, []);

    const handleDownloadClick = async (conversationId: string) => {
        setDownloading(conversationId);
        try {
            const response = await fetch(`${BASE_URL}/downloadConversation?conversationId=${conversationId}`);
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'conversation.json'; 
                document.body.appendChild(a);
                a.click();
                a.remove();
                setShowSuccessAlert(true); 
            } else {
                console.error('Failed to download conversation:', response.statusText);
            }
        } catch (error) {
            console.error('Error during conversation download:', error);
        } finally {
            setDownloading(null); 
        }
    };

    return (
        <Box sx={{ padding: 2 }}>
            <Typography sx={{ fontFamily: 'Dosis' }} variant="h4" gutterBottom>
                Conversations of all users
            </Typography>

            {loading ? (
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
                                    secondaryAction={
                                        <IconButton
                                            edge="end"
                                            aria-label="download"
                                            onClick={() => handleDownloadClick(con.id)}
                                            disabled={downloading === con.id} 
                                        >
                                            {downloading === con.id ? (
                                                <CircularProgress size={24} />
                                            ) : (
                                                <CloudDownloadIcon />
                                            )}
                                        </IconButton>
                                    }
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

            <Snackbar
                open={showSuccessAlert}
                autoHideDuration={3000}
                onClose={() => setShowSuccessAlert(false)}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert onClose={() => setShowSuccessAlert(false)} severity="success" sx={{ width: '100%' }}>
                    Conversation downloaded successfully!
                </Alert>
            </Snackbar>
        </Box>
    );
};

export default DownloadConversations;
