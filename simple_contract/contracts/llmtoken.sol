// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract IntegratedTokenPlatform is ERC20, Ownable {
    uint256 public rate; // Number of tokens received per ETH
    uint256 public startTime; // Fundraising start time
    uint256 public endTime; // Fundraising end time

    struct ApiProvider {
        address providerAddress;
        uint256 earnings; // Earnings in tokens
    }

    mapping(address => ApiProvider) public apiProviders; // API provider information
    mapping(address => bool) public isProvider; // Record if address is a provider

    event TokensPurchased(address indexed buyer, uint256 amount);
    event TokensBurned(address indexed burner, uint256 amount);
    event ApiUsed(address indexed user, address indexed provider, uint256 amount);
    event ProviderAdded(address indexed provider);
    event ProviderRemoved(address indexed provider);

    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply,
        uint256 _rate,
        uint256 _durationInMinutes
    ) ERC20(name, symbol) Ownable() {
        _mint(msg.sender, initialSupply * (10 ** decimals())); // Initial supply to contract owner
        rate = _rate;
        startTime = block.timestamp;
        endTime = startTime + (_durationInMinutes * 1 minutes);
    }

    modifier duringFundraising() {
        require(block.timestamp >= startTime && block.timestamp <= endTime, "Fundraising is not active");
        _;
    }

    modifier afterFundraising() {
        require(block.timestamp > endTime, "Fundraising is still active");
        _;
    }

    modifier onlyProvider() {
        require(isProvider[msg.sender], "Not an API provider");
        _;
    }

    function buyTokens() external payable duringFundraising {
        require(msg.value > 0, "You must send ETH to purchase tokens");

        uint256 tokensToBuy = msg.value * rate;
        require(balanceOf(owner()) >= tokensToBuy, "Not enough tokens available");

        _transfer(owner(), msg.sender, tokensToBuy);
        emit TokensPurchased(msg.sender, tokensToBuy);
    }

    function burnTokens(uint256 ethAmount) external afterFundraising {
        require(ethAmount > 0, "Must burn ETH to receive tokens");
        require(address(this).balance >= ethAmount, "Insufficient ETH balance in contract");

        uint256 tokensToReceive = ethAmount * rate;
        require(balanceOf(owner()) >= tokensToReceive, "Not enough tokens available");

        payable(address(0)).transfer(ethAmount); // Burn ETH
        _transfer(owner(), msg.sender, tokensToReceive);
        emit TokensBurned(msg.sender, tokensToReceive);
    }

    function addApiProvider(address _provider) external onlyOwner {
        require(!isProvider[_provider], "Already a provider");
        isProvider[_provider] = true;
        apiProviders[_provider] = ApiProvider(_provider, 0);
        emit ProviderAdded(_provider);
    }

    function removeApiProvider(address _provider) external onlyOwner {
        require(isProvider[_provider], "Not a provider");
        isProvider[_provider] = false;
        emit ProviderRemoved(_provider);
    }

    function useApi(address _provider, uint256 _amount) external {
        require(isProvider[_provider], "Invalid API provider");
        require(balanceOf(msg.sender) >= _amount, "Insufficient balance");

        _transfer(msg.sender, address(this), _amount);
        apiProviders[_provider].earnings += _amount;
        _transfer(address(this), _provider, _amount);

        emit ApiUsed(msg.sender, _provider, _amount);
    }

    function withdrawEarnings() external onlyProvider {
        uint256 earnings = apiProviders[msg.sender].earnings;
        require(earnings > 0, "No earnings to withdraw");

        apiProviders[msg.sender].earnings = 0;
        _transfer(address(this), msg.sender, earnings);
    }

    function withdrawEth() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    function endFundraising() external onlyOwner {
        require(block.timestamp >= endTime, "Fundraising is still active");
        selfdestruct(payable(owner())); // Destroy contract and send remaining ETH to owner
    }
}