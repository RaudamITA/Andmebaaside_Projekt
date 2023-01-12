import React, { useState, useEffect } from "react";
import "mdb-react-ui-kit/dist/css/mdb.min.css";
import ReactChipInput from "react-chip-input";
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
	MDBRating,
	MDBCheckbox,
	MDBRange,
} from "mdb-react-ui-kit";
import { BrowserRouter as Router } from "react-router-dom";

export default function App() {
	//login popup
	const [loginModal, setloginModal] = useState(false);
	const toggleShowLogin = () => setloginModal(!loginModal);

	//Create Hotel popup
	const [createModal, setCreateModal] = useState(false);
	const toggleShowCreate = () => setCreateModal(!createModal);

	//Create hotel data
	const [hotelName, setHotelName] = useState(null);
	const [hotelStoryCount, setHotelStoryCount] = useState(null);
	const [hotelStars, setHotelStars] = useState(null);
	const [hotelAddress, setHotelAddress] = useState(null);
	const [hotelPhone, setHotelPhone] = useState(null);
	const [hotelEmail, setHotelEmail] = useState(null);
	const [hotelWebsite, setHotelWebsite] = useState(null);
	const [hotelDescription, setHotelDescription] = useState(null);
	const [hotelAmenitiesIn, setHotelAmenitiesIn] = useState([]);
	const [hotelAmenitiesOut, setHotelAmenitiesOut] = useState([]);
	const [hotelImage, setHotelImage] = useState([]);

	//if isLoggedIn and username
	const [fullname, setFullname] = useState(null);
	const [isLoggedIn, setIsLoggedIn] = useState(false);

	useEffect(() => {
		if (
			localStorage.getItem("token") !== "undefined" &&
			localStorage.getItem("token") !== null
		) {
			fetch("http://localhost:8000/users/read/me", {
				method: "GET",
				headers: {
					Authorization: `Bearer ${localStorage.getItem("token")}`,
				},
			})
				.then((response) => response.json())
				.then((response) => {
					setFullname(response.first_name + " " + response.last_name);
					console.log(response);
				});

			setIsLoggedIn(true);
		} else {
			setIsLoggedIn(false);
		}
	}, [toggleShowLogin]);

	//Login input
	const [username, setUsername] = useState(null);
	const [password, setPassword] = useState(null);

	const fetchToken = async (username, password) => {
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

		await fetch("http://localhost:8000/token", options)
			.then((response) => response.json())
			.then((response) =>
				localStorage.setItem("token", response.access_token)
			)

			.catch((err) => console.error(err));

		console.log("Requesting Token");
		toggleShowLogin();
	};

	const logOut = () => {
		localStorage.removeItem("token");
		setIsLoggedIn(false);
	};

	var hotelData = {
		name: hotelName,
		story_count: hotelStoryCount,
		stars: hotelStars,
		address: hotelAddress,
		phone: hotelPhone,
		email: hotelEmail,
		website: hotelWebsite,
		description: hotelDescription,
		amenities_in: hotelAmenitiesIn,
		amenities_out: hotelAmenitiesOut,
		image: hotelImage,
	};

	const createHotel = async (token) => {
		await fetch("http://localhost:8000/hotels/create", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify(hotelData),
		});
	};

	return (
		<>
			<MDBNavbar
				className="m-4"
				dark
				bgColor="dark"
				style={{
					borderRadius: "1rem",
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
					{isLoggedIn === false && (
						<MDBBtn className="mb-0 me-4" onClick={toggleShowLogin}>
							Login
						</MDBBtn>
					)}
					{isLoggedIn && (
						<div className="d-flex align-items-center">
							<p className="text-white mb-0 me-4">{fullname}</p>
							<MDBBtn className="mb-0 me-4" onClick={logOut}>
								Log Out
							</MDBBtn>
							<MDBBtn
								className="mb-0 me-4"
								onClick={toggleShowCreate}
							>
								Create
							</MDBBtn>
						</div>
					)}
				</MDBContainer>
			</MDBNavbar>
			<MDBModal show={loginModal} setShow={setloginModal} tabIndex="-1">
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
											onClick={toggleShowLogin}
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
										<MDBBtn
											className="mt-4 mb-5 mx-2 px-5"
											size="lg"
											onClick={() =>
												fetchToken(username, password)
											}
										>
											Login
										</MDBBtn>
										<div>
											<p className="mb-0">
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
			<MDBModal show={createModal} setShow={setCreateModal} tabIndex="-1">
				<MDBModalBody>
					<MDBContainer fluid>
						<MDBRow className="d-flex justify-content-center align-items-center h-100">
							<MDBCol col="12">
								<MDBCard
									className="bg-dark text-white my-5 mx-auto"
									style={{
										borderRadius: "1rem",
										maxWidth: "75%",
									}}
								>
									<div className="p-2 mx-2">
										<MDBBtn
											className="btn-close mt-3"
											color="light"
											onClick={toggleShowCreate}
										></MDBBtn>
									</div>

									<MDBCardBody className="p-5 d-flex flex-column align-items-center mx-auto w-100">
										<h2 className="fw-bold mb-2 text-uppercase">
											Create Hotel
										</h2>
										<p className="text-white-50 mb-5">
											Please enter your hotel's
											description
										</p>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Hotel's Name"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelName(e.target.value)
											}
										/>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Story Count"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelStoryCount(
													e.target.value
												)
											}
										/>
										<h2>Stars</h2>
										<MDBRange
											defaultValue={2.5}
											min="0"
											max="5"
											step="0.5"
											id="customRange3"
										/>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Address"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelAddress(e.target.value)
											}
										/>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Phone Number"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelPhone(e.target.value)
											}
										/>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Hotel's Email"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelPhone(e.target.value)
											}
										/>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Hotel's Website"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelWebsite(e.target.value)
											}
										/>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Hotel's Description"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelDescription(
													e.target.value
												)
											}
										/>
										<h2>Hotel's Amenities In</h2>
										<div
											className="mb-4"
											style={{ maxWidth: "95%" }}
										></div>

										<h2>Hotel's Amenities Out</h2>
										<div
											className="mb-4"
											style={{ maxWidth: "95%" }}
										>
											<MDBCheckbox
												name="inlineCheck"
												id="inlineCheckbox1"
												value="option1"
												label="1"
												inline
											/>
											<MDBCheckbox
												name="inlineCheck"
												id="inlineCheckbox2"
												value="option2"
												label="2"
												inline
											/>
											<MDBCheckbox
												name="inlineCheck"
												id="inlineCheckbox3"
												value="option3"
												label="3 (disabled)"
												disabled
												inline
											/>
											<MDBCheckbox
												name="inlineCheck"
												id="inlineCheckbox3"
												value="option3"
												label="3 (disabled)"
												disabled
												inline
											/>
											<MDBCheckbox
												name="inlineCheck"
												id="inlineCheckbox3"
												value="option3"
												label="3 (disabled)"
												disabled
												inline
											/>
											<MDBCheckbox
												name="inlineCheck"
												id="inlineCheckbox3"
												value="option3"
												label="3 (disabled)"
												disabled
												inline
											/>
										</div>

										<MDBInput
											className="text-white"
											wrapperClass="mb-4 mx-5 w-100"
											labelClass="text-white"
											label="Hotel's Image (URL)"
											type="text"
											size="lg"
											onChange={(e) =>
												setHotelImage(e.target.value)
											}
										/>

										<MDBBtn
											className="mt-4 mb-5 mx-2 px-5"
											size="lg"
											onClick={() =>
												createHotel(
													localStorage.getItem(
														"token"
													)
												)
											}
										>
											Create
										</MDBBtn>
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
