import React from 'react';
import { colors } from './data';
import ColorDiagram from '../ColorDiagram';
import { Box, TextField, Typography, Slider, Select, MenuItem, Paper } from '@mui/material';

const Controller: React.FC<{
    maxTokens: number;
    setMaxTokens: (value: number) => void;
    systemPrompt: string;
    setSystemPrompt: (value: string) => void;
    model: string;
    setModel: (value: string) => void;
    provider: string, 
    setProvider: (value: string) => void;
}> = ({ maxTokens, setMaxTokens, systemPrompt, setSystemPrompt, model, setModel, provider, setProvider }) => {
    return (
        <Paper 
            sx={{ 
                height: '100%', 
                p: 3, 
                backgroundColor: '#f0f4f8', 
                borderRadius: '15px', 
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                overflowY: 'auto'
            }}
        >
            <Box>
                <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', fontFamily: 'Dosis', color: '#34495e' }}>
                    Settings
                </Typography>
                <Typography variant="h6" sx={{ fontFamily: 'Dosis', fontSize: 15, color: '#2c3e50', mb: 1 }}>
                    True values represent the scale of probabilities.
                </Typography>
                <ColorDiagram colors={colors} />
                
                <Box sx={{ my: 3 }}>
                    <Typography variant="h6" sx={{ fontFamily: 'Dosis', color: '#2c3e50', mb: 1 }}>
                        Max Tokens
                    </Typography>
                    <Slider
                        value={maxTokens}
                        min={1}
                        max={1024}
                        sx={{ color: '#1abc9c' }}
                        onChange={(e, value) => setMaxTokens(value as number)}
                    />
                    <Typography sx={{ color: '#7f8c8d', fontSize: '0.9em', fontFamily: 'Dosis' }}>
                        Current: {maxTokens}
                    </Typography>
                </Box>

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
                        <MenuItem value="openrouter">openrouter</MenuItem>
                        <MenuItem value="togetherai">togetherai</MenuItem>
                    </Select>
                </Box>

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
                        <MenuItem value="gpt-3.5-turbo">GPT-3.5-TURBO</MenuItem>
                        <MenuItem value="gpt-4">GPT-4</MenuItem>
                    </Select>
                </Box>
            </Box>
        </Paper>
    );
};

export default Controller;
