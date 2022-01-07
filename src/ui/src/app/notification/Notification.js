import React, { useState, useEffect } from "react";
import { toast } from 'react-toastify';
import io from "socket.io-client";
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';
import { getConnection } from '../main/connection/connection/store/connectionSlice';
import { getOperation } from '../main/operation/operation/store/dataOperationSlice';
import { getOperationJob } from '../main/operation/job/store/dataOperationJobSlice';

let socket = io.connect(`${window.NOTIFICATION_URI}`);

const Notification = () => {
	const dispatch = useDispatch();
	const history = useHistory();
	const [notifications, setNotifications] = useState([]);


	function GotoComponent(path) {
		history.push('/'.concat(path));
	}
	const getAdditionalDataValue = (additionalData, key) => {
		if (additionalData !== undefined && additionalData?.length > 0) {
			let data = additionalData.filter(e => e.Key === key)
			if (data && data?.length > 0) {
				return data[0].Value
			}
		}
		return null
	}

	const handleClick = (event, notification) => {
		if (notification.AdditionalData && notification.AdditionalData?.length > 0) {
			let id = getAdditionalDataValue(notification.AdditionalData, 'Id')
			let type = getAdditionalDataValue(notification.AdditionalData, 'Type')
			let routePath = ''
			switch (type) {
				case 'ConnectionSql':
					routePath = 'connection/sql'
					if (id && id !== null) {
						routePath += '/' + id
					}
					break;
				case 'ConnectionBigData':
					routePath = 'connection/bigdata'
					if (id && id !== null) {
						routePath += '/' + id
					}
					break;
				case 'DataOperation':
					routePath = 'operation'
					if (id && id !== null) {
						routePath += '/' + id
					}
					break;
				case 'DataOperationJob':
					routePath = 'operationjob'
					if (id && id !== null) {
						routePath += '/' + id
					}
					break;
				default:
					break;
			}
			if (routePath !== '') {
				GotoComponent(routePath)
			}
		}
	};
	const actionSelector = (action, type, id) => {
		switch (type) {
			case 'ConnectionSql':
				{
					let path = '/connection/sql'
					if (action !== 1) {
						path += '/' + id
					}
					if ((window.location.pathname === path)) {
						dispatch(getConnection({ id: id }))
					}
					break;
				}
			case 'ConnectionBigData':
				{
					let path = '/connection/bigdata'
					if (action !== 1) {
						path += '/' + id
					}
					if ((window.location.pathname === path)) {
						dispatch(getConnection({ id: id }))
					}
					break;
				}
			case 'DataOperation':
				{
					let path = '/operation'
					if (action !== 1) {
						path += '/' + id
					}
					if ((window.location.pathname === path)) {
						dispatch(getOperation({ id: id }))
					}
					break;
				}
			case 'DataOperationJob':
				{
					let path = '/operationjob'
					if (action !== 1) {
						path += '/' + id
					}
					if ((window.location.pathname === path)) {
						dispatch(getOperationJob({ id: id }))
					}
					break;
				}
			default:
				break;
		}
	}
	const actions = (notification) => {
		if (!notification.Action || notification.Action == null) {
			return;
		}
		let id = getAdditionalDataValue(notification.AdditionalData, 'Id')
		let type = getAdditionalDataValue(notification.AdditionalData, 'Type')
		switch (notification.Action) {
			case 1:
			case 2:
			case 3:
				actionSelector(notification.Action, type, id)
				break;
			default:
				break;
		}
	};
	const showNotification = (notification) => {
		let notificationContent = (
			<div>
				<h6>
					{notification.Message}
				</h6>
				{
					notification.AdditionalData && notification.AdditionalData?.length > 0 ? (
						< h6 style={{ color: 'blue' }}
							onClick={(event) => handleClick(event, notification)}
						>
							Redirect To Page
						</h6>
					) : ('')
				}
			</div >
		)

		if (notification.Type === 1) {
			toast.success(notificationContent, { position: toast.POSITION.BOTTOM_RIGHT })
		}
		else if (notification.Type === 2) {
			toast.error(notificationContent, { position: toast.POSITION.BOTTOM_RIGHT })
		}
		else if (notification.Type === 3) {
			toast.warn(notificationContent, { position: toast.POSITION.BOTTOM_RIGHT })
		}
		else if (notification.Type === 4) {
			toast.info(notificationContent, { position: toast.POSITION.BOTTOM_RIGHT })
		}
		else if (notification.Type === 5) {
			toast(notificationContent, { position: toast.POSITION.BOTTOM_RIGHT })
		}
	};

	const getNotifications = () => {
		socket.on("notification", notification => {
			if (notification && notification != null) {
				actions(notification)
				showNotification(notification)
				setNotifications([...notifications, notification]);
			}
		});
	};

	useEffect(() => {
		getNotifications();
	}, []);

	return (
		""
	)
}
export default Notification;