
ifLocal = true
ifDebugex = false

// const types = [
// 	'ACT_ACQUIRE', // 0
// 	'ACT_RELEASE',
// 	'ACT_BROADCAST',
// 	'ACT_AUTH',
// 	'ACT_SYNC',
// 	'ACT_CHANGE_MODE', // 5
// 	'STAT_AUTH_SUCC',
// 	'STAT_AUTH_FAIL',
// 	'STAT_INPUT',
// 	'STAT_OUTPUT',
// 	'STAT_UPLOADED', // 10
// 	'STAT_DOWNLOADED',
// 	'STAT_PROGRAMMED',
// 	'STAT_DOWNLOAD_FAIL',
// 	'OP_BTN_DOWN',
// 	'OP_BTN_UP', // 15
// 	'OP_SW_OPEN',
// 	'OP_SW_CLOSE',
// 	'OP_PROG',
// 	'INFO_USER_CHANGED',
// 	'INFO_DISCONN', //20
// 	'INFO_BROADCAST',
// 	'INFO_MODE_CHANGED',
// 	'INFO_VIDEO_URL',
// 	'KEY_DOWN',
// 	'KEY_UP', //25
//
// 	'SYNC_DEVICE',
// ]

const types = [
	'WHO_YOU_ARE',
    'AUTH_USER',
    'AUTH_SUCC_USER',
    'AUTH_FAIL_USER',
    'AUTH_DEVICE',
    'AUTH_SUCC_DEVICE',
    'UPDATE_DEVICE',
    'UPDATE_DEVICE_SUCC',
    'ACT_SYNC',
    'SYNC_DEVICE',

    'ACT_ACQUIRE',
    'ACT_SYNC_SW_BTN',
    'ACT_SYNC_SW_BTN_SUCC',
    'INIT_FILE_UPLOAD',
    'INIT_FILE_UPLOAD_SUCC',
    'ACQUIRE_FAIL',
    'ACQUIRE_SUCC',
    'ACQUIRE_DEVICE_FOR_EXP',
    'ACQUIRE_DEVICE_SUCC_EXP',
	'ACQUIRE_DEVICE_FOR_TEST',
    'ACQUIRE_DEVICE_SUCC_TEST',

    'ACT_RELEASE',

    'REQ_SEG',
    'REQ_SEG_SUCC',
    'REQ_LED',
    'REQ_LED_SUCC',
	'REQ_READ_DATA',
    'REQ_READ_DATA_SUCC',

    'OP_PROGRAM',
    'OP_PROGRAM_SUCC',

    'OP_SW_OPEN',
    'OP_SW_CLOSE',
    'OP_SW_OPEN_DEVICE',
    'OP_SW_CLOSE_DEVICE',
    'OP_SW_CHANGED',

    'OP_BTN_PRESS',
    'OP_BTN_RELEASE',
    'OP_BTN_PRESS_DEVICE',
    'OP_BTN_RELEASE_DEVICE',
    'OP_BTN_CHANGED',

    'OP_PS2_SEND',
    'OP_PS2_SEND_SUCC',

	'AUTH_RABBIT',
    'AUTH_RABBIT_SUCC',
	'AUTH_RABBIT_FAIL',

	'AUTH_RABBIT',
    'AUTH_RABBIT_SUCC',
    'AUTH_RABBIT_FAIL',
	'TEST_PROGRAM',
	'TEST_PROGRAM_SUCC',
	'TEST_PROGRAM_FAIL',
	'TEST_READ_RESULT',
	'TEST_READ_RESULT_SUCC',
]

const typelist = {}

types.forEach((val, index) => {
	/*
	 * note that this statement will be executed
	 * in ES5 environment.
	 */
	 typelist[val] = index
})

let socketMy = null
let device_id = "0"

/*store.subscribe(() => {
	const states = store.getState()
	const newdeviceid = states.device.deviceID
	if ( newdeviceid !== device_id ) {
		device_id = newdeviceid
		reconnect_socket()
	} else {
		console.log(newdeviceid)
	}
})*/

const mlocation = {
	host: 'exotic.zjusig.com'
}
const llocation = {
	host: '47.96.95.218:30040'
}

let mylocation = null
if ( ifLocal ) {
	mylocation = llocation
} else {
	mylocation = mlocation
}

// export const detect_newdevice = (platform, newdeviceid) => {
// 	device_id = newdeviceid
// 	reconnect_socket(platform)
// 	if (ifDebugex) console.log(newdeviceid)
// }

function testLJW() {
	// socket = new WebSocket(`ws://${mylocation.host}/socket/device0`)
	socketMy = new WebSocket(`ws://${mylocation.host}`)
	socketMy.onopen = (event) => {
		// remote.sync()
		//store.dispatch(showOpstatus(platform, ('设备获取成功,设备号: '+String(device_id))))
		// if (ifDebugex) console.log('设备获取成功,设备号' + device_id)
		// remote.auth_user()
	}
	socketMy.onmessage = (event) => {
		if (ifDebugex) console.log('recv message :',event.data)
		const data = JSON.parse(event.data)
		switch (data.type){
			case typelist.WHO_YOU_ARE:{
				remote.auth_user()
				break
			}
			case typelist.AUTH_SUCC_USER: {
				if (ifDebugex) console.log(data.content)
				remote.sync();
				break
			}
			case typelist.SYNC_DEVICE: {
				if (ifDebugex) console.log(data.content)
				nReady = data.content.nReady;
				nBusy = data.content.nBusy;
				nError = data.content.nError;
				break
			}
			case typelist.AUTH_FAIL_USER: {
				if (ifDebugex) console.log("error in auth: " + data.content)
				break
			}
			case typelist.ACQUIRE_SUCC: {
				if (ifDebugex) console.log("成功获取设备: " + data.content)
				device_id = data.content.device
				break
			}
			case typelist.ACT_RELEASE: {
				if (ifDebugex) console.log("设备掉线，请重新连接: " + data.content)
				socketMy.close()
				break
			}
			case typelist.OP_SW_CHANGED: {
				// console.log(data.content)
				 // console.log("老的SW: " + SWState)
				SWState[data.content.id] = data.content.changeTo
				 // console.log("新的SW: " + SWState)
				showSW2()
				break
			}
			case typelist.OP_BTN_CHANGED: {
				// console.log("老的BTN: " + BTNState)
				BTNState[data.content.id] = data.content.changeTo
				// console.log("新的BTN: " + BTNState)
				showBTN2()
				// TODO 按钮信号在press后只能立马释放否则存在歧义
				break
			}
			case typelist.OP_PS2_SEND_SUCC: {
				if (ifDebugex) console.log("PS2 send ok")
				break
			}
			case typelist.ACT_SYNC_SW_BTN_SUCC: {
				for(let i=0; i<data.content.SWState.length; i++){
					SWState[i] = data.content.SWState[i]
				}
				for(let i=0; i<data.content.BTNState.length; i++){
					BTNState[i] = data.content.BTNState[i]
				}
				showSW2()
				showBTN2()
				break
			}
			case typelist.OP_PROGRAM_SUCC: {
				burnBit2_succ()
				upDate_SEG_LED()
				break
			}
			case typelist.REQ_SEG_SUCC: {
				// console.log('seg')
				// console.log(data.seg)
				changeSegMent(data.seg)
				break
			}
			case typelist.REQ_LED_SUCC: {
				// console.log('led')
				// console.log(data.led)
				changeLedState(data.led)
				break
			}
			case typelist.REQ_READ_DATA_SUCC:{
				// console.log(data)
				changeSegMent(data.seg)
				changeLedState(data.led)
				setTimeout(function(){remote.req_SEG_LED();}, 1999);
				break;
			}
		}
		// console.log(data)
		// switch (data.type) {
		// 	case typelist.INFO_USER_CHANGED: {
		// 		const state = store.getState()
		// 		const user = state.account.user
		// 		const occupied = state.device.occupied
		// 		const acquired = state.device.acquired
		// 		if ( data.user === user ) {
		// 			if ( !occupied && !acquired ) {
		// 				store.dispatch(fpgaStatus(true, true))
		// 				store.dispatch(displayError('get ctrl succ'))
		// 			} else {
		// 				store.dispatch(displayError('already yours'+' O'+String(occupied)+' A'+String(acquired)))
		// 			}
		// 		} else if ( data.user === null ) {
		// 			if ( /*occupied &&*/ acquired ) {
		// 				store.dispatch(fpgaStatus(false, false))
		// 				store.dispatch(displayError('release ctrl succ'))
		// 			}
		// 		} else { // other user is using
		// 			if ( !occupied ) {
		// 				store.dispatch(fpgaStatus(false, true))
		// 				store.dispatch(displayError('it has been occupied'))
		// 			}
		// 		}
		// 		break
		// 	}
		// 	case typelist.INFO_DISCONN: {
		// 		break
		// 	}
		// 	case typelist.INFO_BROADCAST: {
		// 		store.dispatch(addBullet(data.content))
		// 		break
		// 	}
		// 	case typelist.STAT_OUTPUT: {
		// 		if (ifDebugex) console.log(data.segs, data.led)
		// 		store.dispatch(updateOutput(data.segs, data.led))
		// 		break
		// 	}
		// 	case typelist.STAT_INPUT: {
		// 		store.dispatch(updateInput(data.buttons, data.switches))
		// 		break
		// 	}
		// 	case typelist.STAT_DOWNLOADED: {
		// 		store.dispatch(showYexpstatus('上传成功'))
		// 		store.dispatch(toggleUpload(true))
		// 		break
		// 	}
		// 	case typelist.STAT_DOWNLOAD_FAIL: {
		// 		store.dispatch(showYexpstatus('上传失败，请重试'))
		// 		store.dispatch(toggleUpload(false))
		// 		break
		// 	}
		// 	case typelist.STAT_PROGRAMMED: {
		// 		store.dispatch(showYexpstatus('烧录成功'))
		// 		store.dispatch(toggleUpload(false)) // once programmed, reset
		// 		break
		// 	}
		// 	case typelist.INFO_MODE_CHANGED: {
		// 		if (ifDebugex) console.log('change to ',data.mode)
		// 		break
		// 	}
		// 	case typelist.INFO_VIDEO_URL: {
		// 		delete data.type
		// 		store.dispatch(updateVideoUrl(data))
		// 		break
		// 	}
		// 	default:
		// 		if (ifDebugex) console.log(data)
		// }
	}
	socketMy.onclose = (event) => {
		if (ifDebugex) console.log('关闭设备' + device_id)
	}
	socketMy.onerror = (event) =>{
		if (ifDebugex) console.log("Error: " + event.name + " " + event.number)
	}

}

function send(obj){
	if (ifDebugex) console.log(obj)
	if (ifDebugex) console.log("ljw")
	if (socketMy.readyState === WebSocket.OPEN) {
		if (ifDebugex) console.log(obj)
		if (ifDebugex) console.log(JSON.stringify(obj))
		socketMy.send(JSON.stringify(obj))
	} else {
		//store.dispatch(showYexpstatus('无法连接设备，请重新获取'))
		//store.dispatch(fpgaStatus(false, false)) // regard as disconnected
		console.log('无法连接设备，请重新获取')
	}
}

const remote = {
	auth_user: () => {
		send({
			type: typelist.AUTH_USER
		})
	},
	sync: () => {
		send({
			type: typelist.ACT_SYNC
		})
	},
	sync_SW_BTN: () => {
		send({
			type: typelist.ACT_SYNC_SW_BTN
		})
	},
	acquire: () => {
		if (ifDebugex) console.log('acquire')
		send({
			type: typelist.ACT_ACQUIRE,
			using: "exp"
		})
	},
	release: () => {
		if (ifDebugex) console.log('release')
		send({
			type: typelist.ACT_RELEASE,
			content: {
				device: device_id,
			}
		})
	},
	req_SEG: () => {
		if (ifDebugex) console.log('req_SEG')
		send({
			type: typelist.REQ_SEG
		})
	},
	req_LED: () => {
		if (ifDebugex) console.log('req_LED')
		send({
			type: typelist.REQ_LED
		})
	},
	req_SEG_LED: () => {
		if (ifDebugex) console.log('req_SEG_LED')
		send({
			type: typelist.REQ_READ_DATA
		})
	},
	openSwitch: (id) => {
		if (ifDebugex) console.log('open sw :',id)
		send({
			type: typelist.OP_SW_OPEN,
			content: {
				id: id
			}
		})
	},
	closeSwitch: (id) => {
		if (ifDebugex) console.log('close sw :',id)
		send({
			type: typelist.OP_SW_CLOSE,
			content: {
				id: id
			}
		})
	},
	pressButton: (id) => {
		if (ifDebugex) console.log('set btn :', id)
		send({
			type: typelist.OP_BTN_PRESS,
			content: {
				id: id
			}
		})
	},
	releaseButton: (id) => {
		if (ifDebugex) console.log('reset btn :', id)
		send({
			type: typelist.OP_BTN_RELEASE,
			content: {
				id: id
			}
		})
	},
	sendPS2: (byte) => {
		send({
			type: typelist.OP_PS2_SEND,
			content: {
				byte: byte
			}
		})
	},
	initFileUploaded: (userId, type, expId) => {
		send({
			type: typelist.INIT_FILE_UPLOAD,
			content: {
				userId: userId,
				type: type,
				expId: expId
			}
		})
	},
	program: (userId, type, expId, isUpload, bitFileName) => {
		console.log(userId, type, expId, isUpload, bitFileName)
		compileId = bitFileName.split('.')[0]
		send({
			type: typelist.OP_PROGRAM,
			content: {
				userId: userId,
				type: type,
				expId: expId,
				isUpload: isUpload,
				compileId: compileId,
				bitFileName: bitFileName
			}
		})
	},
	// changeDispmode: (mode) => {
	// 	if (mode !== 'video' && mode !== 'digital')
	// 			return
	// 	send({
	// 		type: typelist.ACT_CHANGE_MODE,
	// 		mode
	// 	})
	// },
	// broadcast: (content) => {
	// 	if (ifDebugex) console.log('broadcast: ',content)
	// 	send({
	// 		type: typelist.ACT_BROADCAST,
	// 		content
	// 	})
	// },
}

// export const reconnect_socket = (platform) => {
// 	try {
// 		if (socket.readyState === WebSocket.OPEN) {
// 			socket.close()
// 		}
// 		if ( ifLocal ) {
// 			if (ifDebugex) console.log('socket')
// 			return
// 		} else if (!device_id) {
// 			if (ifDebugex) console.log(' empty device id ')
// 			return
// 		} else {
// 			socket = new WebSocket(`ws://${location.host}/socket/${device_id}`)
// 		}
// 	} catch (e) {
// 		//store.dispatch(displayError('cannot connect with server'))
// 		store.dispatch(showOpstatus(platform, ('设备获取失败,请重试')))
// 		console.log('设备获取失败,请重试')
// 		return
// 	}
// 	socket.onopen = (event) => {
// 		remote.sync()
// 		//store.dispatch(showOpstatus(platform, ('设备获取成功,设备号: '+String(device_id))))
// 		console.log('设备获取成功,设备号')
// 	}
// 	socket.onmessage = (event) => {
// 		if (ifDebugex) console.log('recv message :',event.data)
// 		const data = JSON.parse(event.data)
// 		switch (data.type) {
// 			case typelist.INFO_USER_CHANGED: {
// 				const state = store.getState()
// 				const user = state.account.user
// 				const occupied = state.device.occupied
// 				const acquired = state.device.acquired
// 				if ( data.user === user ) {
// 					if ( !occupied && !acquired ) {
// 						store.dispatch(fpgaStatus(true, true))
// 						store.dispatch(displayError('get ctrl succ'))
// 					} else {
// 						store.dispatch(displayError('already yours'+' O'+String(occupied)+' A'+String(acquired)))
// 					}
// 				} else if ( data.user === null ) {
// 					if ( /*occupied &&*/ acquired ) {
// 						store.dispatch(fpgaStatus(false, false))
// 						store.dispatch(displayError('release ctrl succ'))
// 					}
// 				} else { // other user is using
// 					if ( !occupied ) {
// 						store.dispatch(fpgaStatus(false, true))
// 						store.dispatch(displayError('it has been occupied'))
// 					}
// 				}
// 				break
// 			}
// 			case typelist.INFO_DISCONN: {
// 				break
// 			}
// 			case typelist.INFO_BROADCAST: {
// 				store.dispatch(addBullet(data.content))
// 				break
// 			}
// 			case typelist.STAT_OUTPUT: {
// 				if (ifDebugex) console.log(data.segs, data.led)
// 				store.dispatch(updateOutput(data.segs, data.led))
// 				break
// 			}
// 			case typelist.STAT_INPUT: {
// 				store.dispatch(updateInput(data.buttons, data.switches))
// 				break
// 			}
// 			case typelist.STAT_DOWNLOADED: {
// 				store.dispatch(showYexpstatus('上传成功'))
// 				store.dispatch(toggleUpload(true))
// 				break
// 			}
// 			case typelist.STAT_DOWNLOAD_FAIL: {
// 				store.dispatch(showYexpstatus('上传失败，请重试'))
// 				store.dispatch(toggleUpload(false))
// 				break
// 			}
// 			case typelist.STAT_PROGRAMMED: {
// 				store.dispatch(showYexpstatus('烧录成功'))
// 				store.dispatch(toggleUpload(false)) // once programmed, reset
// 				break
// 			}
// 			case typelist.INFO_MODE_CHANGED: {
// 				if (ifDebugex) console.log('change to ',data.mode)
// 				break
// 			}
// 			case typelist.INFO_VIDEO_URL: {
// 				delete data.type
// 				store.dispatch(updateVideoUrl(data))
// 				break
// 			}
// 			default:
// 				if (ifDebugex) console.log(data)
// 		}
// 	}
// }
//
// const send = (obj) => {
// 	if (socket.readyState === WebSocket.OPEN) {
// 		if (ifDebugex) console.log(obj)
// 		socket.send(JSON.stringify(obj))
// 	} else {
// 		store.dispatch(showYexpstatus('无法连接设备，请重新获取'))
// 		store.dispatch(fpgaStatus(false, false)) // regard as disconnected
// 	}
// }
//
// export const remote = {
// 	sync: () => {
// 		send({
// 			type: typelist.ACT_SYNC
// 		})
// 	},
// 	broadcast: (content) => {
// 		if (ifDebugex) console.log('broadcast: ',content)
// 		send({
// 			type: typelist.ACT_BROADCAST,
// 			content
// 		})
// 	},
// 	acquire: () => {
// 		if (ifDebugex) console.log('acquire')
// 		send({
// 			type: typelist.ACT_ACQUIRE
// 		})
// 	},
// 	release: () => {
// 		if (ifDebugex) console.log('release')
// 		send({
// 			type: typelist.ACT_RELEASE
// 		})
// 	},
// 	openSwitch: (id) => {
// 		if (ifDebugex) console.log('open sw :',id)
// 		send({
// 			type: typelist.OP_SW_OPEN,
// 			id
// 		})
// 	},
// 	closeSwitch: (id) => {
// 		if (ifDebugex) console.log('close sw :',id)
// 		send({
// 			type: typelist.OP_SW_CLOSE,
// 			id
// 		})
// 	},
// 	pressButton: (id) => {
// 		if (ifDebugex) console.log('set btn :', id)
// 		send({
// 			type: typelist.OP_BTN_DOWN,
// 			id
// 		})
// 	},
// 	releaseButton: (id) => {
// 		if (ifDebugex) console.log('reset btn :', id)
// 		send({
// 			type: typelist.OP_BTN_UP,
// 			id
// 		})
// 	},
// 	fileUploaded: () => {
// 		send({
// 			type: typelist.STAT_UPLOADED
// 		})
// 	},
// 	program: () => {
// 		send({
// 			type: typelist.OP_PROG
// 		})
// 	},
// 	changeDispmode: (mode) => {
// 		if (mode !== 'video' && mode !== 'digital')
// 				return
// 		send({
// 			type: typelist.ACT_CHANGE_MODE,
// 			mode
// 		})
// 	}
// }
//
