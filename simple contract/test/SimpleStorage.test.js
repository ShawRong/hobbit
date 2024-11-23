const SimpleToken = artifacts.require("SimpleToken");

contract("SimpleToken", (accounts) => {
    let simpleTokenInstance;

    before(async () => {
        // 部署合约
        simpleTokenInstance = await SimpleToken.new(1000); // 设定初始供应量为 1000
    });

    it("should get the balance of an address", async () => {
        const address = accounts[0]; // 使用第一个账户地址
        const balance = await simpleTokenInstance.getBalance(address);
        console.log("Balance:", balance.toString());
        
        // 你可以在这里添加断言来验证余额
        assert.equal(balance.toString(), "1000", "Initial balance should be 1000");
    });
});