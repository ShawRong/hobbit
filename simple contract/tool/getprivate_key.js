const Web3 = require('web3');
const HDWalletProvider = require('@truffle/hdwallet-provider');

const mnemonic = 'your twelve word mnemonic here';
const provider = new HDWalletProvider(mnemonic, 'http://127.0.0.1:8545');
const web3 = new Web3(provider);

async function getAccountsAndPrivateKeys() {
    const accounts = await web3.eth.getAccounts();
    console.log('Accounts:', accounts);

    for (let account of accounts) {
        const privateKey = provider.wallets[account].privateKey;
        console.log(`Account: ${account}, Private Key: ${privateKey}`);
    }
}

getAccountsAndPrivateKeys();