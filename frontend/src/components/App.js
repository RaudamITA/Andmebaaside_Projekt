import React, { useState, useEffect } from "react";
import "mdb-react-ui-kit/dist/css/mdb.min.css";
import {
	MDBNavbar,
	MDBContainer,
	MDBNavbarBrand,
	MDBNavbarToggler,
	MDBNavbarItem,
	MDBNavbarLink,
	MDBCollapse,
	MDBBtn,
	MDBIcon,
	MDBNavbarNav,
	MDBInputGroup,
} from "mdb-react-ui-kit";
import { BrowserRouter as Router } from "react-router-dom";
import Login from "./Login.js";

export default function App() {
	const [user, setUser] = useState(null);
	const [isLoggedIn, setIsLoggedIn] = useState(false);

	useEffect(() => {
		if (localStorage.getItem("token") !== "undefined") {
			setIsLoggedIn(true);
		}
	}, []);

	console.log(localStorage.getItem("token"));

	return isLoggedIn ? (
		<MDBNavbar dark bgColor="dark">
			<MDBContainer fluid>
				<MDBNavbarBrand>Hotel</MDBNavbarBrand>
				<MDBInputGroup tag="form" className="d-flex w-auto mb-3 mt-3">
					<input
						className="form-control"
						placeholder="Search"
						aria-label="Search"
						type="Search"
					/>
					<MDBBtn outline>Search</MDBBtn>
				</MDBInputGroup>
				<MDBBtn outline className="me-2" type="button">
					Log in
				</MDBBtn>
			</MDBContainer>
		</MDBNavbar>
	) : (
		<Login />
	);
}
