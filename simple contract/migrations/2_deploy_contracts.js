const IntegratedTokenPlatform = artifacts.require("IntegratedTokenPlatform");

module.exports = function(deployer) {
    deployer.deploy(IntegratedTokenPlatform, 'LLM Coin', 'llmc', 100000000, 10, 10000)
        .then(instance => {
            console.log("IntegratedTokenPlatform deployed at address:", instance.address);
        });
};