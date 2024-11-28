import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const login = async () => {
        try {
            const response = await axios.post('http://localhost:5000/login', { email, password });
            alert(response.data.message);
        } catch (error) {
            alert('Login failed');
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
            <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
            <button onClick={login}>Login</button>
        </div>
    );
}

export default App;
