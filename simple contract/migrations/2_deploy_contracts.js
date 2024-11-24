const IntegratedTokenPlatform = artifacts.require("IntegratedTokenPlatform");

module.exports = async function(deployer, network, accounts) {
    // 使用 accounts[0] 作为部署账户
    await deployer.deploy(
        IntegratedTokenPlatform, 
        'LLM Coin', 
        'llmc', 
        100000000, 
        10, 
        10000,
        { from: accounts[0] }  // 明确指定部署账户
    );
    
    const instance = await IntegratedTokenPlatform.deployed();
    console.log("IntegratedTokenPlatform deployed at address:", instance.address);
};