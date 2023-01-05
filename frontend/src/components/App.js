import { useState } from "react";
import Login from "./Login.js";

export default function App() {
	const [user, setUser] = useState(null);
	const [isLoggedIn, setIsLoggedIn] = useState(false);

	if (user !== null) {
		setIsLoggedIn(true);
	}

	return isLoggedIn ? <div>no login</div> : <Login />;
}
