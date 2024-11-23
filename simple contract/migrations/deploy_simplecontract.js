const Simple = artifacts.require("SimpleToken");

module.exports = function(deployer) {
    deployer.deploy(Simple);
};