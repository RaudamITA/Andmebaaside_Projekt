import React, { useState, useEffect } from "react";
import {
	MDBContainer,
	MDBRow,
	MDBCol,
	MDBCard,
	MDBCardBody,
	MDBInput,
	MDBBtn,
	MDBModal,
	MDBModalBody,
} from "mdb-react-ui-kit";

interface ChildProps {
	fetchToken: Function;
}

const Login = (props: ChildProps) => {
	//login popup
	const [loginModal, setloginModal] = useState(false);
	const toggleShowLogin = () => setloginModal(!loginModal);

	//Login input
	const [username, setUsername] = useState(null);
	const [password, setPassword] = useState(null);

	return (
		<>
			<MDBBtn className="mb-0 me-4" onClick={toggleShowLogin}>
				Login
			</MDBBtn>
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
												props.fetchToken(
													username,
													password
												)
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
		</>
	);
};

export default Login;
