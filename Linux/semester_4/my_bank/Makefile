all:
	g++ initializer.cpp -o initializer
	g++ client.cpp bank_options.cpp -o client
	g++ deinitializer.cpp -o deinitializer

test_display_all:
	./initializer 4 100 
	./client 4 < test_files/display_all.txt
	./deinitializer

test_freeze_account_1_display_and_test:
	./initializer 4 100
	./client 4 < test_files/freeze_account.txt
	./deinitializer

test_transfer_1_to_2_accounts_10_dollar:
	./initializer 4 100
	./client 4 < test_files/transfer.txt
	./deinitializer

test_add_money_to_acounts_and_checkMaximumBalance_and_withdraw_sameAmount:
	./initializer 4 100
	./client 4 < test_files/add_money.txt
	./deinitializer

destroy_shared_memory:
	./deinitializer
clean:
	rm initializer deinitializer client