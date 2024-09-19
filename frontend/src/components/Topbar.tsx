import React from 'react';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import { AppBar, Toolbar, Typography } from '@mui/material';

const Topbar: React.FC = () => {
  return (
    <AppBar position="static" sx={{ flex: 0 }}>
      <Toolbar>
        <AccountTreeIcon sx={{ mx: 1, fontSize: 25 }} />
        <Typography variant="h6" sx={{ fontFamily: 'Dosis' }}>
            Hallucination-Checker 
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Topbar;

