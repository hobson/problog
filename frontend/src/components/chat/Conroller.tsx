import React, { useState } from 'react';
import { colors } from './data';
import { Link } from 'react-router-dom';
import { BASE_URL } from '../../api/api';
import ColorDiagram from '../ColorDiagram';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import DeleteIcon from '@mui/icons-material/Delete';
import { Box, TextField, Typography, Slider, Select, MenuItem, Paper, Button, CircularProgress, IconButton } from '@mui/material';

const Controller: React.FC<{
    maxTokens: number;
    setMaxTokens: (value: number) => void;
    systemPrompt: string;
    setSystemPrompt: (value: string) => void;
    model: string;
    setModel: (value: string) => void;
    provider: string;
    setProvider: (value: string) => void;
    createNewConversation: any;
    file: any;
    setFile: any;
    usernameMatch: boolean;
    conversationTitle: string;
    changeConversationTitle: any;
}> = ({ maxTokens, setMaxTokens, systemPrompt, setSystemPrompt, model, setModel, provider, setProvider, createNewConversation, file, setFile, usernameMatch, conversationTitle, changeConversationTitle }) => {
    const [uploadFile, setUploadFile] = useState<File | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [uploadSuccess, setUploadSuccess] = useState<boolean | null>(null);

    const [isEditing, setIsEditing] = useState(false);
    const [tempTitle, setTempTitle] = useState(conversationTitle);

    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleSaveClick = () => {
        changeConversationTitle(tempTitle)
        setIsEditing(false);
    };

    const handleCancelClick = () => {
        setTempTitle(conversationTitle);
        setIsEditing(false); 
    };

    // Handle file selection
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files?.[0];
        if (selectedFile) {
            setUploadFile(selectedFile);
            setUploadSuccess(null);
        }
    };

    // Handle file upload
    const handleFileUpload = async () => {
        if (!uploadFile) return;
        setLoading(true);
        const conversationId: any = localStorage.getItem('conversationId');
        const formData = new FormData();
        formData.append('file', uploadFile);
        formData.append('conversation_id', conversationId);

        try {
            const response = await fetch(`${BASE_URL}/uploadFile`, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                setUploadSuccess(true);
                setFile({ fileId: data.file_id, fileTitle: data.file_title });
            } else {
                setUploadSuccess(false);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            setUploadSuccess(false);
        } finally {
            setLoading(false);
        }
    };

    // Handle file deletion with confirmation
    const handleDeleteFile = async () => {
        if (window.confirm("Are you sure you want to delete this file?")) {
            if (!file.fileId) return;

            try {
                const response = await fetch(`${BASE_URL}/deleteFile`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ fileId: file.fileId }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert(data.message);
                    setFile({});
                    setUploadFile(null);
                } else {
                    alert(data.error || 'Error deleting the file.');
                }
            } catch (error) {
                console.error('Error deleting file:', error);
                alert('Failed to delete the file.');
            }
        }
    };

    const date = new Date(Date.now());
    const formattedDate = `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;

    return (
        <Paper
            sx={{
                height: '100%',
                p: 3,
                backgroundColor: '#f0f4f8',
                borderRadius: '15px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                overflowY: 'auto',
            }}
        >
            <Box>
                <Box>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography variant="h5" sx={{ mb: 3, fontSize: 18, fontWeight: 400, fontFamily: 'Dosis', color: '#000000' }}>
                            Conversation name:
                        </Typography>
                        {usernameMatch && (
                            !isEditing && (
                                <EditIcon sx={{ cursor: "pointer", fontSize: 30, mx: 1 }} onClick={handleEditClick} />
                            )
                        )}
                    </Box>

                    {usernameMatch && (
                        isEditing && (
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <TextField
                                    value={tempTitle}
                                    onChange={(e) => setTempTitle(e.target.value)}
                                    variant="outlined"
                                    size="small"
                                    sx={{ fontSize: 18, fontFamily: 'Dosis' }}
                                    autoFocus
                                />
                                <IconButton onClick={handleSaveClick} sx={{ ml: 1, color: 'green' }}>
                                    <CheckIcon />
                                </IconButton>
                                <IconButton onClick={handleCancelClick} sx={{ color: 'red' }}>
                                    <CloseIcon />
                                </IconButton>
                            </Box>
                        )
                    )}
                </Box>
                <Typography variant="h5" sx={{ mb: 3, fontSize: 18, fontWeight: 400, fontFamily: 'Dosis', color: '#34495e' }}>
                    {conversationTitle ? conversationTitle : 'No Conversation name yet'}
                </Typography>
                <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', fontFamily: 'Dosis', color: '#34495e' }}>
                    Settings
                </Typography>
                <Typography variant="h6" sx={{ fontFamily: 'Dosis', fontSize: 15, color: '#2c3e50', mb: 1 }}>
                    True values represent the scale of probabilities.
                </Typography>
                <ColorDiagram colors={colors} />

                {/* All Conversations and Create New Conversation Buttons */}
                <Box>
                    <Link to={"/conversations"}>
                        <Button fullWidth variant='outlined' sx={{ my: 1, fontFamily: 'Dosis' }}>
                            All Conversations
                        </Button>
                    </Link>
                    {usernameMatch && (
                        <Button onClick={createNewConversation} fullWidth variant='outlined' sx={{ my: 1, fontFamily: 'Dosis' }}>
                            Create new Conversation +
                        </Button>
                    )}
                </Box>

                {/* Max Tokens */}
                <Box sx={{ my: 3 }}>
                    <Typography variant="h6" sx={{ fontFamily: 'Dosis', color: '#2c3e50', mb: 1 }}>
                        Max Tokens
                    </Typography>
                    <Slider
                        value={maxTokens}
                        min={1}
                        max={1024}
                        sx={{ color: '#1abc9c' }}
                        onChange={(_, value) => setMaxTokens(value as number)}
                    />
                    <Typography sx={{ color: '#7f8c8d', fontSize: '0.9em', fontFamily: 'Dosis' }}>
                        Current: {maxTokens}
                    </Typography>
                </Box>

                {/* System Prompt */}
                <Box sx={{ my: 3 }}>
                    <Typography variant="h6" sx={{ color: '#2c3e50', mb: 1, fontFamily: 'Dosis' }}>
                        System Prompt
                    </Typography>
                    <TextField
                        fullWidth
                        multiline
                        minRows={4}
                        variant="outlined"
                        value={systemPrompt}
                        onChange={(e) => setSystemPrompt(e.target.value)}
                        sx={{ backgroundColor: '#ecf0f1', borderRadius: '10px', fontFamily: 'Dosis' }}
                    />
                </Box>

                {/* Provider Select */}
                <Box sx={{ my: 3 }}>
                    <Typography variant="h6" sx={{ color: '#2c3e50', fontFamily: 'Dosis', mb: 1 }}>
                        Provider
                    </Typography>
                    <Select
                        fullWidth
                        value={provider}
                        onChange={(e) => setProvider(e.target.value as string)}
                        sx={{ backgroundColor: '#ecf0f1', borderRadius: '10px' }}
                    >
                        <MenuItem value="openai">openai</MenuItem>
                        {/* <MenuItem value="openrouter">openrouter</MenuItem> */}
                    </Select>
                </Box>

                {/* Model Select */}
                <Box sx={{ my: 3 }}>
                    <Typography variant="h6" sx={{ color: '#2c3e50', fontFamily: 'Dosis', mb: 1 }}>
                        Model
                    </Typography>
                    <Select
                        fullWidth
                        value={model}
                        onChange={(e) => setModel(e.target.value as string)}
                        sx={{ backgroundColor: '#ecf0f1', borderRadius: '10px' }}
                    >
                        <MenuItem value="gpt-4o-2024-08-06">GPT-4o-2024-08-06</MenuItem>
                        <MenuItem value="gpt-4o-2024-05-13">GPT-4o-2024-05-13</MenuItem>
                        <MenuItem value="chatgpt-4o-latest">ChatGPT-4o-Latest {formattedDate}</MenuItem>
                        <MenuItem value="gpt-4o-mini">GPT-4o-Mini</MenuItem>
                        <MenuItem value="gpt-4o-mini-2024-07-18">GPT-4o-Mini-2024-07-18</MenuItem>
                        <MenuItem value="gpt-4-turbo-2024-04-09">GPT-4-Turbo-2024-04-09</MenuItem>
                        <MenuItem value="gpt-4-turbo-preview">GPT-4-Turbo-Preview</MenuItem>
                        <MenuItem value="gpt-4-0125-preview">GPT-4-0125-Preview</MenuItem>
                        <MenuItem value="gpt-4-1106-preview">GPT-4-1106-Preview</MenuItem>
                        <MenuItem value="gpt-4">GPT-4</MenuItem>
                        <MenuItem value="gpt-4-0613">GPT-4-0613</MenuItem>
                        <MenuItem value="gpt-3.5-turbo-0125">GPT-3.5-Turbo-0125</MenuItem>
                        <MenuItem value="gpt-3.5-turbo">GPT-3.5-Turbo</MenuItem>
                        <MenuItem value="gpt-3.5-turbo-1106">GPT-3.5-Turbo-1106</MenuItem>
                    </Select>

                </Box>

                {usernameMatch && (
                    Object.keys(file).length > 0 ? (
                        <Box>
                            <Typography variant="h6" sx={{ color: '#2c3e50', fontFamily: 'Dosis', mb: 1 }}>
                                Uploaded file
                            </Typography>
                            <Box sx={{ display: 'flex', flexDirection: 'row', gap: 1 }}>
                                <Typography variant="h6" sx={{ color: '#2c3e50', fontFamily: 'Dosis', mb: 1 }}>
                                    {file.fileTitle}.csv
                                </Typography>
                                <DeleteIcon
                                    sx={{ fontSize: 30, color: 'red', cursor: 'pointer' }}
                                    onClick={handleDeleteFile}
                                />
                            </Box>
                        </Box>
                    ) : (
                        <Box>
                            <Typography variant="h6" sx={{ color: '#2c3e50', fontFamily: 'Dosis', mb: 1 }}>
                                File Upload
                            </Typography>
                            <Button
                                variant="outlined"
                                component="label"
                                sx={{ fontFamily: 'Dosis', borderRadius: '10px', backgroundColor: '#ecf0f1', mx: 1 }}
                            >
                                Choose File
                                <input type="file" hidden onChange={handleFileChange} />
                            </Button>

                            <Button
                                variant="contained"
                                color="primary"
                                onClick={handleFileUpload}
                                disabled={loading || !uploadFile}
                                sx={{ fontFamily: 'Dosis' }}
                            >
                                {loading ? <CircularProgress size={24} /> : 'Upload'}
                            </Button>
                            {uploadSuccess && <Typography color="green">Upload successful!</Typography>}
                            {uploadSuccess === false && <Typography color="red">Upload failed.</Typography>}
                        </Box>
                    )
                )}
            </Box>
        </Paper>
    );
};

export default Controller;
