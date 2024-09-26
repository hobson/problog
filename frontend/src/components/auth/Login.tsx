import React, { useState } from 'react';
import { Box, Button, Container, TextField, Typography, Modal, Backdrop, Fade } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const handleClose = () => setOpen(false);

  const handleLogin = async () => {
    if (!username || !password) {
      setError('Username and password are required');
      setOpen(true);
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        username,
        password,
      });

      
      if (response.data.message === 'Login successful') {
        localStorage.setItem('username', username);
        navigate('/');  
      }
    } catch (error: any) {
      if (error.response && error.response.data.error) {
        
        setError(error.response.data.error);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
      setOpen(true);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          bgcolor: '#f5f5f5',
          padding: 4,
          borderRadius: 2,
        }}
      >
        <Typography sx={{ fontFamily: 'Dosis' }} variant="h4" gutterBottom>
          Login
        </Typography>
        <Box component="form" sx={{ mt: 1, width: '100%' }} onSubmit={(e) => e.preventDefault()}>
          <TextField
            fullWidth
            label="Username"
            variant="outlined"
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            variant="outlined"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 3, mb: 2, fontFamily: 'Dosis' }}
            onClick={handleLogin}
          >
            Login
          </Button>
          <Typography variant="body2" sx={{ textAlign: 'center', mt: 2, fontFamily: 'Dosis' }}>
            Don't have an account?{' '}
            <Link to="/register">
              Register here
            </Link>
          </Typography>
        </Box>
      </Box>

      {/* Error Modal */}
      <Modal
        open={open}
        onClose={handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={open}>
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: 400,
              bgcolor: 'background.paper',
              border: '2px solid #000',
              boxShadow: 24,
              p: 4,
              textAlign: 'center',
            }}
          >
            <Typography variant="h6" sx={{ mb: 2 }}>
              Error
            </Typography>
            <Typography variant="body1">{error}</Typography>
            <Button onClick={handleClose} variant="contained" color="primary" sx={{ mt: 2 }}>
              Close
            </Button>
          </Box>
        </Fade>
      </Modal>
    </Container>
  );
};

export default Login;
