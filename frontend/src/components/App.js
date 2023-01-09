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
	MDBRow,
	MDBCol,
	MDBCard,
	MDBCardBody,
	MDBInput,
	MDBBtn,
	MDBIcon,
	MDBNavbarNav,
	MDBInputGroup,
	MDBModal,
	MDBModalDialog,
	MDBModalContent,
	MDBModalHeader,
	MDBModalTitle,
	MDBModalBody,
	MDBModalFooter,
} from "mdb-react-ui-kit";
import { BrowserRouter as Router } from "react-router-dom";
import Login from "./Login.js";

export default function App() {
	const [basicModal, setBasicModal] = useState(false);
	const toggleShow = () => setBasicModal(!basicModal);

	const [user, setUser] = useState(null);
	const [isLoggedIn, setIsLoggedIn] = useState(false);

	useEffect(() => {
		if (localStorage.getItem("token") !== "undefined") {
			setIsLoggedIn(true);
		}
	}, []);

	const [username, setUsername] = useState(null);
	const [password, setPassword] = useState(null);

	const fetchToken = (username, password) => {
		if (username === null || password === null) {
			return;
		}
		const options = {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: new URLSearchParams({
				grant_type: "password",
				username: username,
				password: password,
			}),
		};

		fetch("http://localhost:8000/token", options)
			.then((response) => response.json())
			.then((response) =>
				localStorage.setItem("token", response.access_token)
			)
			.catch((err) => console.error(err));

		console.log("ma olen taun ja ma küsisin millegi pärast tokenit");
	};

	console.log(localStorage.getItem("token"));

	return (
		<>
			<MDBNavbar dark bgColor="dark">
				<MDBContainer fluid>
					<MDBNavbarBrand>Hotel</MDBNavbarBrand>
					<MDBInputGroup
						tag="form"
						className="d-flex w-auto mb-3 mt-3"
					>
						<input
							className="form-control"
							placeholder="Search"
							aria-label="Search"
							type="Search"
						/>
						<MDBBtn outline>Search</MDBBtn>
					</MDBInputGroup>
					<MDBBtn onClick={toggleShow}>Log In</MDBBtn>
				</MDBContainer>
			</MDBNavbar>
			<MDBModal show={basicModal} setShow={setBasicModal} tabIndex="-1">
				<MDBModalBody>
					<MDBContainer fluid>
						<MDBRow className="d-flex justify-content-center align-items-center h-100">
							<MDBCol col="12">
								<MDBCard
									className="bg-dark text-white my-5 mx-auto"
									style={{
										borderRadius: "1rem",
										maxWidth: "400px",
									}}
								>
									<div className="p-2 mx-2">
										<MDBBtn
											className="btn-close mt-3"
											color="light"
											onClick={toggleShow}
										></MDBBtn>
									</div>

									<MDBCardBody className="p-5 d-flex flex-column align-items-center mx-auto w-100">
										<h2 className="fw-bold mb-2 text-uppercase">
											Login
										</h2>
										<p className="text-white-50 mb-5">
											Please enter your login and
											password!
										</p>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Username"
											type="text"
											size="lg"
											onChange={(e) =>
												setUsername(e.target.value)
											}
										/>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Password"
											type="password"
											size="lg"
											onChange={(e) =>
												setPassword(e.target.value)
											}
										/>

										<p className="small mb-3 pb-lg-2">
											<a
												className="text-white-50"
												href="#!"
											>
												Forgot password?
											</a>
										</p>
										<MDBBtn
											className="mx-2 px-5"
											size="lg"
											onClick={fetchToken(
												username,
												password
											)}
										>
											Login
										</MDBBtn>
										<div>
											<p className="mt-5 mb-0">
												Don't have an account?{" "}
												<a
													href="/register"
													className="text-white-50 fw-bold"
												>
													Sign Up
												</a>
											</p>
										</div>
									</MDBCardBody>
								</MDBCard>
							</MDBCol>
						</MDBRow>
					</MDBContainer>
				</MDBModalBody>
			</MDBModal>
		</>
	);
}
