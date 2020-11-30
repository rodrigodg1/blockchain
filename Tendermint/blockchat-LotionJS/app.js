// app.js
let lotion = require('lotion')


async function main() {



    let app = lotion({
        initialState: {

            messages: [
                {sender:'Rodrigo', message:'Chat Seguro' }
           
            ]

        },

        //keyPath: './privkey.json',       // path to privkey.json. generates own keys if not specified.
        //genesisPath: './genesis.json',   // path to genesis.json. generates new one if not specified.
        logTendermint: false,          // if true, shows all output from the underlying tendermint process
        p2pPort: 26658,                // port to use for tendermint peer connections
        rpcPort: 26657



    })




    app.use(function (state, tx) {


	
        if (
	    typeof tx.sender === 'string' &&
            typeof tx.message === 'string' &&
            tx.message.length <= 50
        ) {

            if (tx.message !== '') {
                state.messages.push({
		    sender: tx.sender,
                    message: tx.message
                });
            }
        }




    })

    app.start().then(function (appInfo) {
        console.log(`app started. gci: ${appInfo.GCI}`)
    })



}

main()
