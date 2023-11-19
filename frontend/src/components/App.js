import React, { useState, useEffect } from 'react';
import 'mdb-react-ui-kit/dist/css/mdb.min.css';
import CreateHotel from './CreateHotel';
import Login from './Login';
import {
	MDBNavbar,
	MDBContainer,
	MDBNavbarBrand,
	MDBNavbarToggler,
	MDBNavbarItem,
	MDBNavbarLink,
	MDBInput,
	MDBBtn,
	MDBNavbarNav,
	MDBInputGroup,
} from 'mdb-react-ui-kit';
import { BrowserRouter as Router } from 'react-router-dom';

export default function App() {
	//login popup
	const [loginModal, setloginModal] = useState(false);
	const toggleShowLogin = () => setloginModal(!loginModal);

	//if isLoggedIn and username
	const [fullname, setFullname] = useState(null);
	const [isLoggedIn, setIsLoggedIn] = useState(false);

	useEffect(() => {
		if (
			localStorage.getItem('token') !== 'undefined' &&
			localStorage.getItem('token') !== null
		) {
			fetch('http://0.0.0.0:8000/users/read/me', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				},
			})
				.then((response) => response.json())
				.then((response) => {
					setFullname(response.first_name + ' ' + response.last_name);
					console.log(response);
				});

			setIsLoggedIn(true);
		} else {
			setIsLoggedIn(false);
		}
	}, [toggleShowLogin]);

	const fetchToken = async (username, password) => {
		if (username === null || password === null) {
			return;
		}
		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: new URLSearchParams({
				grant_type: 'password',
				username: username,
				password: password,
			}),
		};

		await fetch('http://0.0.0.0:8000/token', options)
			.then((response) => response.json())
			.then((response) =>
				localStorage.setItem('token', response.access_token)
			)

			.catch((err) => console.error(err));

		console.log('Requesting Token');
		toggleShowLogin();
	};

	const logOut = () => {
		localStorage.removeItem('token');
		setIsLoggedIn(false);
	};

	return (
		<>
			<MDBNavbar
				className="m-4"
				dark
				bgColor="dark"
				style={{
					borderRadius: '1rem',
				}}
			>
				<MDBContainer fluid>
					<MDBNavbarBrand>Hotels</MDBNavbarBrand>
					<MDBInputGroup
						tag="form"
						className="d-flex w-auto mb-3 mt-3"
					>
						<input
							className="form-control"
							placeholder="Hotels.."
							aria-label="Search"
							type="Search"
						/>
						<MDBBtn outline>Search</MDBBtn>
					</MDBInputGroup>
					{isLoggedIn === false && <Login fetchToken={fetchToken} />}
					{isLoggedIn && (
						<div className="d-flex align-items-center">
							<p className="text-white mb-0 me-4">{fullname}</p>
							<MDBBtn className="mb-0 me-4" onClick={logOut}>
								Log Out
							</MDBBtn>
							<CreateHotel />
						</div>
					)}
				</MDBContainer>
			</MDBNavbar>
		</>
	);
}
