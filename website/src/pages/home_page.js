import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import { Widget, addResponseMessage } from 'react-chat-widget';
import Button from '@mui/material/Button';
import RefreshIcon from '@mui/icons-material/Refresh';
import {WS_BASE, API_BASE} from '../consts/urls';

function HomePage({ }) {
    const [help_requests, setHelpRequests] = useState([])
    const [socket, setSocket] = useState('')
    let userId = 11

    const connectAgent = (client_id) => {
        let socket = new WebSocket(`${WS_BASE}ws/agent/${userId}/client/${client_id}`);
        socket.onmessage = (event) => {
            var data = JSON.parse(event.data);
            console.log(data)
             if (data.data.content) {
                addResponseMessage(data.data.content)
                console.log(data.data.content)
            }
        }
        setSocket(socket)
    }

    const getList = () => {
        return fetch(API_BASE + 'users/help-required', {
                method: 'GET',
            }
        ).then((res) => {
            return res.json()
        }).then((res) => {
            console.log(res)
            setHelpRequests(res.data)
        })
    }


    const SimpleList = () => (
        <div>
            <h2>
                Refresh List <Button style={{marginLeft: 20}} variant="contained" color="primary" onClick={() => getList()}><RefreshIcon/></Button>
            </h2>

            { help_requests && help_requests.map(client =>
                <Box sx={{ flexGrow: 1 }} key={client.id} >
                    {client.username}
                    <Button style={{marginLeft: 20}} onClick={()=>connectAgent(client.id)} variant="text" color="primary">Assist Client</Button>
                </Box>
            )}
        </div>
    );

    const getCustomLauncher = (handleToggle) =>
        <button id="button_hid" style={{ display: "None" }} onClick={handleToggle}>This is my launcher component!</button>

    useEffect(() => {
        document.getElementById("button_hid").click()
        getCustomLauncher()
        getList()
    }, []);

    const handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // Now send the message throught the backend API
        socket.send(JSON.stringify({'content': newMessage, 'content_type': 'text'}))
    };

    return (
        <>
            <Box sx={{ flexGrow: 1 }}>
                <div style={{textAlign: 'center'}}>
                    <h1>Flight Assistance Page</h1>
                </div>
            </Box>
            <Box sx={{ flexGrow: 1 }}>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <div style={{ textAlign: 'center' }}>
                            <SimpleList />
                        </div>
                    </Grid>
                    <Grid item xs={8}>
                        <div style={{ textAlign: 'center' }}>
                            <Widget
                                handleNewUserMessage={handleNewUserMessage}
                                title="Chat"
                                subtitle=""
                                launcher={handleToggle => getCustomLauncher(handleToggle)}
                            />
                        </div>
                    </Grid>
                </Grid>
            </Box>
        </>
    );
}

export default HomePage;