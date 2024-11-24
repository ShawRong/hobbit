#document

#some api design
- 
# some summary
2_deploy_contracts.js
=====================

   Deploying 'IntegratedTokenPlatform'
   -----------------------------------
   > transaction hash:    0x188b44c0c9d156605798417e3e67342f65f54284537d703685bea8170c683fa9
   > Blocks: 0            Seconds: 0
   > contract address:    0x116a439b3cf13595225A8d941C2bb76a81Fb51DB
   > block number:        11
   > block timestamp:     1732457957
   > account:             0xdC3cD90D39e1D3A0bD7d713CE314646e0Dc39479
   > balance:             115792089237316195423570985008687907853269984665540564039457.558222798220067703
   > gas used:            2534185 (0x26ab29)
   > gas price:           2.770049117 gwei
   > value sent:          0 ETH
   > total cost:          0.007019816921564645 ETH

IntegratedTokenPlatform deployed at address: 0x116a439b3cf13595225A8d941C2bb76a81Fb51DB
   > Saving artifacts
   -------------------------------------
   > Total cost:     0.007019816921564645 ETH

Summary
=======
> Total deployments:   1
> Final cost:          0.007019816921564645 ETH

# script
   truffle develop
   let accounts = await web3.eth.getAccounts();
   console.log(accounts);

(0) 0x3d47335fd2b7330d90c6b6f674cf0735de094549
(1) 0x77c0222d1c37bd9b6f3e4c93d85485bfcc02979d
(2) 0x5becfe310aae758fded3b17bb7394c3fa20e9496
(3) 0x06a87fe7420a8d67a4f3455ac7ce545981462a22
(4) 0x85511b1b1fa286bbf61823460f8353a9adea7ba3
(5) 0x4fed1bf6b3105c280214ab626358a5161992b1c9
(6) 0xc41df8391b942cfe2656db98875b5b1026a38d50
(7) 0x5887f0531106733b9e1558a42fede950e344720e
(8) 0x728e5f7b83ab3e76471e847ae2b48f16b6f67368
(9) 0x8ae84c2c737d3199a93ab3e83c16e2a7890de972

Private Keys:
(0) 0ad1df7638c948fd3181361d9436e901d0540fde045d02fdc05c208d605277e5
(1) e939bd8998051aae56872b16e7a38433181477a667ed6b5dcacec84360fb185f
(2) 18ec3ec426b6b083c4419908153cc42a15e19de81cd679c00df438985ccf1cfd
(3) 9ff3e38270627ef08d93700a3e47e2f831853f448c0e26d16b37acf52f1088be
(4) f4682a81697f877d0d3e6fbf0b95e566caa0f35ac9fbc11b39184b9a5acfe953
(5) 4a372164e031249f0335ba766ec68b6f83a4c2c8b542397edf83e3b48d045131
(6) a6a0f875b3bf77aad2149500452daca6f475e6ba849cd96f34ba23309c189253
(7) 8d8808ed755fed7f8ca7ccaca4ce1320e136be3f95984329e4c83bc0fc0df1cb
(8) 058a9941df2ae1b84e084daf4d30916e01b6c4f54067611ad13459089dc24d3a
(9) 6a8732a38b3f17e0c27299f164289dabc0bd88b6fbd935be6774343ff3194feb




geth --datadir . --http -http.api "eth,net,web3,personal,miner,admin" --http.corsdomain "" --http.vhosts "" --http.addr '0.0.0.0' --http.port 8545 --dev console --allow-insecure-unlock --keystore . --password password.txt --unlock 57bbec496a82ec51fbffed75eaa91e57e6510e83

truffle migrate --reset --network goeth