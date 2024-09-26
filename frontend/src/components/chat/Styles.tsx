import { Box } from "@mui/material";
import styled from "styled-components";

// ========================== CHAT =====================================>

export const MessageBubble = styled(Box)<{ isuser: boolean }>(({ isuser }) => ({
    backgroundColor: isuser ? '#01426A' : 'F8F8F8',
    color: isuser ? '#fff' : '#000',
    padding: '10px 20px',
    borderRadius: '15px',
    border: '1px solid #01426A',
    maxWidth: '100%',
    alignSelf: isuser ? 'flex-end' : 'flex-start',
    marginBottom: 5,
}));

export const chatContainer = {
    display: 'flex',
    flexDirection: { xs: 'column', md: 'row' },
    flex: 1,
    justifyContent: 'space-between',
    height: '100%',
    padding: 2,
    overflow: 'hidden',
}

export const chatBox = {
    flex: 1,
    width: { xs: '100%', md: '70%' },
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    borderRadius: '8px',
    height: '100%',
    overflow: 'hidden',
}

export const messageContainer = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    borderRadius: '8px',
    overflowY: 'auto',
    padding: 1
}

export const messageText = { fontFamily: 'Dosis' }

export const form = { display: 'flex', alignItems: 'center' }
export const sendIcon = { marginLeft: 1 }

// ==================================== CONTORLLER =================================>

export const controllerContainer = { 
    display: { xs: 'none', md: 'block' }, 
    width: '30%', 
    paddingLeft: 2, 
    height: '100%' 
}

export const drawer = { width: 250, padding: 2 }

export const menu = { 
    position: 'absolute', 
    top: 10, 
    right: 16, 
    display: { xs: 'block', md: 'none' } 
}



