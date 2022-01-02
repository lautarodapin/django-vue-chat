const test = async () => {
    const ws = new WebSocket('ws://localhost:8000/ws/chats/') 
    ws.onmessage = (e) => console.log('onmessage', e)
    ws.onerror = (e) => console.log('onerror', e)
    
    ws.onopen = () => {
        ws.send(JSON.stringify({
            action: 'subscribe_to_chat',
            id: 4,
            request_id: 100,
        }))
        const doFetch = async  () => {
            const response = await fetch('http://localhost:8000/api/messages/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ddcb6d25af54aceea942e769ad621779a7a26691',
                },
                body: JSON.stringify({
                    text: 'hola mundo',
                    chat: 4,
                }),
            })
            const data = await response.json()
            console.log('data', data)
        }
        doFetch()
    }
}
