const Simple = artifacts.require("SimpleToken");

module.exports = function(deployer) {
    deployer.deploy(Simple, 10000).then(() => {
        console.log("simple token deployed at address:", Simple.address)
    });
};