import React from 'react';
import { Stack } from '@mui/material';
import { Chat, Topbar } from '../components';

const Home: React.FC = () => {
    return (
        <Stack 
            sx={{ 
                height: '100vh', 
                overflowY: 'auto',
                display: 'flex', 
                flexDirection: 'column' 
            }}
        >
            <Topbar />
            <Chat />
        </Stack>
    );
}

export default Home;
