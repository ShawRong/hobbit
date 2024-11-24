const IntegratedTokenPlatform = artifacts.require("IntegratedTokenPlatform");

module.exports = async function(deployer, network, accounts) {
  const deployerAccount = accounts[0];  // 使用第一个可用账户
  console.log('Deploying with account:', deployerAccount);
  
  // 定义构造函数参数
  const name = "LLM Token";
  const symbol = "LLM";
  const initialSupply = web3.utils.toBN('20000');  // 使用 BN 处理大数
  const rate = web3.utils.toBN('100');             // 代币兑换率
  const durationInMinutes = web3.utils.toBN('525600');  // 一年的分钟数
  
  console.log('Deployment parameters:');
  console.log('- Name:', name);
  console.log('- Symbol:', symbol);
  console.log('- Initial Supply:', initialSupply.toString());
  console.log('- Rate:', rate.toString());
  console.log('- Duration (minutes):', durationInMinutes.toString());

  try {
    await deployer.deploy(
      IntegratedTokenPlatform,
      name,
      symbol,
      initialSupply,
      rate,
      durationInMinutes,
      { from: deployerAccount }
    );
    
    const instance = await IntegratedTokenPlatform.deployed();
    console.log('Contract deployed at:', instance.address);
    
    // 验证部署后的参数
    const contractName = await instance.name();
    const contractSymbol = await instance.symbol();
    const contractRate = await instance.rate();
    
    console.log('\nContract verification:');
    console.log('- Name:', contractName);
    console.log('- Symbol:', contractSymbol);
    console.log('- Rate:', contractRate.toString());
    
  } catch (error) {
    console.error('\nDeployment Error Details:');
    console.error(error);
    throw error;
  }
};