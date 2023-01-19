import React, { useState } from "react";
import StarRating from "./StarRating";
import Tags from "./Tags";
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

export default function CreateHotel() {
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

	//	Create Hotel popup
	const [createModal, setCreateModal] = useState(false);
	const toggleShowCreate = () => setCreateModal(!createModal);

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
		url: hotelImage,
	};

	const createHotel = async (token) => {
		await fetch("http://localhost:8000/hotels/create", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify(hotelData),
		})
			.then((res) => {
				res.json();
			})
			.then((data) => console.log(data));
		toggleShowCreate();
	};

	return (
		<>
			<MDBBtn className="mb-0 me-4" onClick={toggleShowCreate}>
				Create
			</MDBBtn>
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
										<StarRating
											HotelStars={setHotelStars}
										/>

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
											type="number"
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
										<Tags /* Need work*/ />
										<h2>Hotel's Amenities Out</h2>
										<Tags /* Need work*/ />
										<div
											className="mb-4"
											style={{ maxWidth: "95%" }}
										></div>

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
