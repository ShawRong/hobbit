const IntegratedTokenPlatform = artifacts.require("IntegratedTokenPlatform");

module.exports = async function(deployer, network, accounts) {
  // 指定要使用的账户地址
  const deployerAccount = "0x57BBEC496A82eC51fBFFED75Eaa91E57e6510E83";  // 例如：0x1234...
  
  console.log('Deploying with account:', deployerAccount);
  
  await deployer.deploy(
    IntegratedTokenPlatform,
    "LLM Token",
    "LLM",
    1000,  // initialSupply
    10,    // rate
    1440,  // durationInMinutes
    { 
      from: deployerAccount,
      gas: 5000000,
      gasPrice: web3.utils.toWei('1', 'gwei')
    }
  );
};
